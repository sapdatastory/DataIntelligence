OpenAPI Servlow/Client Operator 처리 예제
===

# 1. Plain Greeter
## 1.1 OpenAPI Servlow Operator : message <-> message
![](images/1.FilePython.png)<br>
OpenAPI Servloe --> Wiretap --> JS

Base Path : /samples/plain_greeter

```javascript
$.setPortCallback("input",onInput);

// for simplicity, no 
var count = 0;
var totalgreeted = 0;
var greeted = {};

function isByteArray(data) {
    return (typeof data === 'object' && Array.isArray(data) 
        && data.length > 0 && typeof data[0] === 'number')
}

function randomBoolean() {
    return Math.random() < 0.5;
}

function sendResponse(s, m, e) {
    if ($.output == null) {
        // invoke the callback directly
        $.sendResponse(s, m, e);
    } else {
        // let the subsequent operator decide what to do
        if (e !== null) {
            m.Attributes["message.response.error"] = e;
        }
        $.output(m);
    }
}

function onInput(ctx,s) {
    var msg = {};

    var inbody = s.Body;
    var inattributes = s.Attributes;
    
    // convert the body into string if it is bytes
    if (isByteArray(inbody)) {
        inbody = String.fromCharCode.apply(null, inbody);
    }

    // prepare for a response message
    msg.Attributes = {};
    for (var key in inattributes) {
        // only copy the headers that won't interfer with the recieving operators
        if (key.indexOf("openapi.header") < 0 || key === "openapi.header.x-request-key") {
             msg.Attributes[key] = inattributes[key];
        }
    }

    // send the response
    var reqmethod = inattributes["openapi.method"];
    var reqpath = inattributes["openapi.request_uri"];
    
    // as there is no swagger spec configured to specify the responese content-type, set it here
    msg.Attributes["openapi.header.content-type"] = "application/json";
    
    switch (reqpath) {
        case "/samples/plain_greeter/v1/ping":
            msg.Body = {"pong": count++};
            sendResponse(s, msg, null);
            break;
        case "/samples/plain_greeter/v1/echo":
            msg.Body = {"echo": inbody};
            sendResponse(s, msg, null);
            break;
        case "/samples/plain_greeter/v1/happy":
            if (randomBoolean()) {
                msg.Body = {"status": "happy"};
            } else {
                msg.Attributes["openapi.status_code"] = 400;
                msg.Body = {"status": "unhappy"};
            }
            sendResponse(s, msg, null);
            break;
        default:
            sendResponse(s, msg, Error("Unexpected operation at " + reqpath))
            break;
    }
}
```

## 1.2 OpenAPI Client Operator : message <-> message
![](images/1.FilePython.png)<br>
Message Generator --> OpenAPI Client --> JS

Host : host:port<br>
Schemes : https<br>
Base Path : /app/pipeline-modeler/openapi/service/samples/plain_greeter<br>
Method : GET

```javascript
// This operator is needed to keep compatibility to the old datagenerator
var counter = 0;

var ping_sample = {"operation":"ping"};
var echo_sample = {"operation":"echo"};
var happy_sample = {"operation": "happy"};

var operations = [ping_sample, echo_sample, happy_sample];

var echochoices = ["hola", "hallo", "hello", "bonjour", "namaste", "merhaba", "konchiwa"];

getRandomChoice = function(choices) {
    return choices[Math.floor(Math.random() * choices.length)];
};

generateMessage = function() {
    var msg = {};
    msg.Attributes = {};
    // add x-requested-with header to pass the vsystem's csrf check
    msg.Attributes["openapi.header_params.x-requested-with"] = "XMLHttpRequest";

    var opchoice = operations[counter % operations.length];
    switch (opchoice["operation"]) {
        case "ping":
            msg.Attributes["openapi.consumes"] = "";
            msg.Attributes["openapi.produces"] = "application/json";
            msg.Attributes["openapi.method"] = "GET";
            msg.Attributes["openapi.path_pattern"] = "/v1/ping";
            break;
        case "echo":
            msg.Body = getRandomChoice(echochoices);
            msg.Attributes["openapi.consumes"] = "text/plain";
            msg.Attributes["openapi.produces"] = "application/json";
            msg.Attributes["openapi.method"] = "POST";
            msg.Attributes["openapi.path_pattern"] = "/v1/echo";
            break;
        case "happy":
            msg.Attributes["openapi.consumes"] = "";
            msg.Attributes["openapi.produces"] = "application/json";
            msg.Attributes["openapi.method"] = "GET";
            msg.Attributes["openapi.path_pattern"] = "/v1/happy";
            break;
    }
    msg.Attributes["message.request.id"] = opchoice["operation"] + "-" + counter;

    counter++;
    return msg;
}

$.addTimer("2000ms",doTick);

function doTick(ctx) {
    $.output(generateMessage());
}
```

# 2. Greeter(with swagger)
## 2.1 OpenAPI Servlow Operator : message <-> message
![](images/1.FilePython.png)<br>
OpenAPI Servloe --> Wiretap --> JS

Base Path : /samples/greeter

```javascript
$.setPortCallback("input",onInput);

// for simplicity, no 
var count = 0;
var totalgreeted = 0;
var greeted = {};

function isByteArray(data) {
    return (typeof data === 'object' && Array.isArray(data) 
        && data.length > 0 && typeof data[0] === 'number')
}

function sendResponse(s, m, e) {
    if ($.output === null) {
        // invoke the callback directly
        $.sendResponse(s, m, e);
    } else {
        // let the subsequent operator decide what to do
        if (e !== null) {
            m.Attributes["message.response.error"] = e;
        }
        $.output(m);
    }
}

function publish(s, ssrid, to, body) {
    var msg = {};
    msg.Attributes = {
        "openapi.header.x-request-key": ssrid,
        "openapi.responder.publish": to
    };
    msg.Body = body;
    sendResponse(s, msg, null);
}

function onInput(ctx,s) {
    var msg = {};

    var inbody = s.Body;
    var inattributes = s.Attributes;
    
    // convert the body into string if it is bytes
    if (isByteArray(inbody)) {
        inbody = String.fromCharCode.apply(null, inbody);
    }

    // prepare for a response message
    msg.Attributes = {};
    for (var key in inattributes) {
        // only copy the headers that won't interfer with the recieving operators
        if (key.indexOf("openapi.header") < 0 || key === "openapi.header.x-request-key") {
             msg.Attributes[key] = inattributes[key];
        }
    }
    
    // build the response
    var reqmethod = inattributes["openapi.method"];
    var reqpath = inattributes["openapi.request_uri"];
    var opid = inattributes["openapi.operation_id"];

    switch (opid) {
        case "ping":
            msg.Body = {"pong": count++};
            sendResponse(s, msg, null);
            break;
        case "echo":
            msg.Body = {"echo": inbody};
            sendResponse(s, msg, null);
            break;
        case "getGreetSummary":
            msg.Body = {"greeted": Object.keys(greeted), "total": totalgreeted};
            sendResponse(s, msg, null);
            break;
        case "getGreetStatus":
            gname = inattributes["openapi.path_params.name"];
            gcount = greeted[gname];
            if (gcount === undefined) {
                gcount = 0;
            }
            msg.Body = {"count": gcount, "name": gname};
            sendResponse(s, msg, null);
            break;
        case "greet":
            gname = inattributes["openapi.path_params.name"];
            ssrid = inattributes["openapi.header.x-request-key"];
            gcount = greeted[gname];
            if (gcount === undefined) {
                gcount = 0;
            }
            gcount++;
            totalgreeted++;
            greeted[gname] = gcount;
            jsonbody = JSON.parse(inbody);
            bodyname = jsonbody["name"];
            bodytext = jsonbody["text"];
            if (bodyname === undefined || bodytext === undefined) {
                sendResponse(s, msg, Error("Invalid body. Missing name or text"))
            } else {
                msg.Body = {"from": gname, "to": bodyname, "text": bodytext};
                sendResponse(s, msg, null);
                if (ssrid !== undefined) {
                    publish(s, ssrid, bodyname, msg.Body);
                }
            }
            break;
        case "upload":
            gname = inattributes["openapi.path_params.name"];
            filename = inattributes["openapi.file_params.file#name"];
            filecontent = inattributes["openapi.file_params.file"];
            // for now, just return the name of the file and the size of the base64 content
            msg.Body = {"name": filename, "size": filecontent.length};
            sendResponse(s, msg, null);
            break;
        case "subscribe":
            gname = inattributes["openapi.path_params.name"];
            ssrid = inattributes["openapi.header.x-request-key"];
            // subscribe is enabled when a request uses swaggersocket and has this id.
            if (ssrid !== undefined) {
                msg.Attributes["openapi.responder.reuse.name"] = gname;
                msg.Attributes["openapi.responder.reuse.hello"] = {"from": gname, "text": "hello", "to": "*"}
                msg.Attributes["openapi.responder.reuse.bye"] = {"from": gname, "text": "bye", "to": "*"}
            }
            msg.Body = [];
            sendResponse(s, msg, null);
            break;
        case "unsubscribe":
            sid = inattributes["openapi.path_params.sid"];
            ssrid = inattributes["openapi.header.x-request-key"];
            // unsubscribe is enabled when a request uses swaggersocket and has this id.
            if (ssrid !== undefined) {
                msg.Attributes["openapi.responder.release"] = sid;
            }
            msg.Body = {"greeted": Object.keys(greeted), "total": totalgreeted};
            sendResponse(s, msg, null);
            break;
        default:
            sendResponse(s, msg, Error("Unexpected operation ID " + opid))
            break;
    }
}
```

## 2.2 OpenAPI Client Operator : message <-> message
![](images/1.FilePython.png)<br>
Message Generator --> JS --> OpenAPI Servloe --> Wiretap

Host : host:port<br>
Schemes : https<br>
Base Path : /app/pipeline-modeler/openapi/service/samples/greeter<br>
Method : GET

```javascript
// This operator is needed to keep compatibility to the old datagenerator
var counter = 0;

// toggle upload_sample if the referenced file is available, otherwise the graph fails.
var upload_sample = {"operation":"upload","name":"logo","file":"operators/com/sap/openapi/client/openapi_logo.svg"};
var upload_sample2 = {"operation":"upload","name":"reme","file":"RXhhbXBsZSBmb3Igb3BlbmFwaS5jbGllbnQgaW52b2tpbmcgdGhlIHZmbG93IGRlbW8gZ3JlZXRlciBzZXJ2aWNlIHdpdGggaXRzIGFwaSBtb2RlbHMKPT09PT09PT09PT0KIyMjIyBEZXNjcmlwdGlvbgpUaGUgb3BlbmFwaS5jbGllbnQgb3BlcmF0b3IgY2FuIGNhbGwgYXJiaXRyYXJ5IFJFU1Qgc2VydmljZXMgZnJvbSBhIGdyYXBoLgoKIyMjIyBQcmVyZXF1aXNpdGVzCiogTm9uZQoKIyMjIyBDb25maWd1cmUgYW5kIFJ1biB0aGUgR3JhcGgKRm9sbG93IHRoZSBzdGVwcyBiZWxvdyB0byBydW4gdGhlIGV4YW1wbGUgZnJvbSB0aGUgRGF0YSBQaXBlbGluZSBVSToKCjEuIFN0YXJ0IHRoZSBvcGVuYXBpLnNlcnZlciBncmVldGVyIGRlbW8gZ3JhcGggKGNvbS5zYXAuZGVtby5vcGVuYXBpLnNlcnZlci5ncmVldGVyKSwgd2hpY2ggZXhwb3NlcyBpdHMgc2VydmljZSBhdCBwYXRoIC9vcGVuYXBpL3NlcnZpY2Uvc2FtcGxlcy9ncmVldGVyIHJlbGF0aXZlIHRvIHRoZSB2ZmxvdyBpbnN0YW5jZSBVUkwuCgoyLiBWZXJpZnkgdGhlIGhvc3QgYW5kIHBvcnQgY29uZmlndXJlZCBmb3IgdGhpcyBkZW1vIGdyYXBoIG1hdGNoZXMgdGhlIGFjdHVhbCB2ZmxvdyBpbnN0YW5jZS4KCjMuIFN0YXJ0IHRoaXMgZGVtbyBncmFwaCwgd2hpY2ggc3RhcnRzIGludm9raW5nIGEgc2VyaWVzIG9mIG9wZXJhdGlvbnMuCgo0LiBPcGVuIHRoZSBVSSBmcm9tIHRoZSB3aXJldGFwIG9wZXJhdG9yIHNvIHRoYXQgdGhlIHJlc3BvbnNlIG1lc3NhZ2VzIGZyb20gdGhlIGludm9rZWQgb3BlcmF0aW9ucyBhcmUgZGlzcGxheWVkIG9uIHRoZSBicm93c2VyLgoKPGJyPgo8ZGl2IGNsYXNzPSJmb290ZXIiPqCgCiAgICZjb3B5OyAyMDE4IFNBUCBTRSBvciBhbiBTQVAgYWZmaWxpYXRlIGNvbXBhbnkuIEFsbCByaWdodHMgcmVzZXJ2ZWQuCjwvZGl2Pgo=", "file#name":"README.txt"};
var ping_sample = {"operation":"ping"};
var echo_sample = {"operation":"echo","body":"string"};
var getGreetSummary_sample = {"operation":"getGreetSummary"};
var getGreetStatus_sample = {"operation":"getGreetStatus","name":"string"};
var greet_sample = {"operation":"greet","name":"string","body":{"name": "string","text": "string"}};

var operations = [ping_sample, echo_sample, greet_sample, getGreetStatus_sample, getGreetSummary_sample, upload_sample, upload_sample2];

var echochoices = ["hola", "hallo", "hello", "bonjour", "namaste", "merhaba", "konchiwa"];
var vocals = "aeiouy";
var consonants = " bcdfghjklmnpqrstvwxz";

getRandomChoice = function(choices) {
    return choices[Math.floor(Math.random() * choices.length)];
};

getRandomName = function(n) {
    var v = "";
    for (i = 0; i < n; i++) {
        v = v + getRandomChoice(consonants) + getRandomChoice(vocals);
    }
    return v;
}

generateMessage = function() {
    var msg = {};
    msg.Attributes = {};
    var opchoice = operations[counter % operations.length];
    switch (opchoice["operation"]) {
        case "ping":
            break;
        case "echo":
            opchoice["body"] = getRandomChoice(echochoices);
            break;
        case "greet":
            opchoice["name"] = getRandomName(2);
            opbody = opchoice["body"];
            opbody["name"] = getRandomName(2);
            opbody["text"] = getRandomChoice(echochoices);
            break;
        case "getGreetStatus":
            opchoice["name"] = getRandomName(2);
            break;
        case "getGreetSummary":
            break;
        case "upload":
            break;
    }
    msg.Attributes["message.request.id"] = opchoice["operation"] + "-" + counter;
    msg.Body = opchoice;

    counter++;
    return msg;
}

$.addTimer("2000ms",doTick);

function doTick(ctx) {
    $.output(generateMessage());
}
```

```go
// go language
package main

import (
	"encoding/json"
	"strings"
)

func main() {}

var (
	count = 0
	totalgreeted = 0
	greeted = make(map[string]int)
)

var Output func(interface{})

func greetednames() []string {
	r := make([]string, len(greeted))
	i := 0
	for k := range greeted {
		r[i] = k
		i++
	}
	return r
}

func decodeJSON(v interface{}) map[string]interface{} {
	var r map[string]interface{}
	switch c := v.(type) {
	case string:
		json.Unmarshal([]byte(c), &r)
	case []byte:
		json.Unmarshal(c, &r)
	case map[string]interface{}:
		r = c
	}
	return r
}

func getstring(m map[string]interface{}, k string) string {
	if v, ok := m[k].(string); ok {
		return v
	} else if v, ok := m[k].([]byte); ok {
		return string(v)
	}
	return ""
}
func getbytes(m map[string]interface{}, k string) []byte {
	if v, ok := m[k].(string); ok {
		return []byte(v)
	} else if v, ok := m[k].([]byte); ok {
		return v
	}
	return []byte{}
}

func send(attrs map[string]interface{}, body interface{}) {
	if (Output == nil) {
		// ignore
	} else {
		// let the subsequent operator decide what to do
		m := make(map[string]interface{})
		m["Attributes"] = attrs
		m["Body"] = body
		Output(m)
	}
}

func publish(ssrid string, to string, body interface{}) {
	m := make(map[string]interface{})
	m["Attributes"] = map[string]interface{} {
		"openapi.header.x-request-key": ssrid,
		"openapi.responder.publish": to,
	}
	m["Body"] = body
	send(m, nil)
}


func Input(val interface{}) {
	reqbody := getstring(val.(map[string]interface{}), "Body")
	reqattrs := val.(map[string]interface{})["Attributes"].(map[string]interface{})
	respattrs := make(map[string]interface{})
	var respbody interface{}

	for key, value := range reqattrs {
		// only copy the headers that won't interfer with the recieving operators
		if !strings.HasPrefix(key,"openapi.header") || key == "openapi.header.x-request-key" {
			respattrs[key] = value
		}
	}

	// build the response
	opid := getstring(reqattrs, "openapi.operation_id")


	switch (opid) {
	case "ping":
		respbody = map[string]interface{}{"pong": count}
		count++
		send(respattrs, respbody)
	case "echo":
		respbody = map[string]interface{}{"echo": reqbody}
		send(respattrs, respbody)
	case "getGreetSummary":
		respbody = map[string]interface{}{"greeted": greetednames(), "total": totalgreeted}
		send(respattrs, respbody)
	case "getGreetStatus":
		gname := getstring(reqattrs, "openapi.path_params.name")
		gcount := greeted[gname];
		respbody = map[string]interface{}{"count": gcount, "name": gname}
		send(respattrs, respbody)
	case "greet":
		gname := getstring(reqattrs, "openapi.path_params.name")
		ssrid := getstring(reqattrs, "openapi.header.x-request-key")
		gcount := greeted[gname]
		gcount++;
		totalgreeted++
		greeted[gname] = gcount
		jsonbody := decodeJSON(reqbody)
		bodyname := getstring(jsonbody, "name")
		bodytext := getstring(jsonbody, "text")
		if bodyname == "" || bodytext == "" {
			respattrs["message.response.error"] = map[string]interface{}{"message":"Invalid body. Missing name or text", "name":"Error"}
			send(respattrs, respbody)
		} else {
			respbody = map[string]interface{}{"from": gname, "to": bodyname, "text": bodytext};
			send(respattrs, respbody)
			if (ssrid != "") {
				publish(ssrid, bodyname, respbody)
			}
		}
	case "upload":
		filename := getstring(reqattrs, "openapi.file_params.file#name")
		filecontent := getbytes(reqattrs, "openapi.file_params.file")
		// for now, just return the name of the file and the size of the base64 content
		respbody := map[string]interface{}{"name": filename, "size": len(filecontent)}
		send(respattrs, respbody)
	case "subscribe":
		gname := getstring(reqattrs, "openapi.path_params.name")
		ssrid := getstring(reqattrs, "openapi.header.x-request-key")
		// subscribe is enabled when a request uses swaggersocket and has this id.
		if (ssrid != "") {
			respattrs["openapi.responder.reuse.name"] = gname
			respattrs["openapi.responder.reuse.hello"] = map[string]interface{}{"from": gname, "text": "hello", "to": "*"}
			respattrs["openapi.responder.reuse.bye"] = map[string]interface{}{"from": gname, "text": "bye", "to": "*"}
		}
		respbody = []interface{}{}
		send(respattrs, respbody)
	case "unsubscribe":
		sid := getstring(reqattrs,"openapi.path_params.sid")
		ssrid := getstring(reqattrs,"openapi.header.x-request-key")
		// unsubscribe is enabled when a request uses swaggersocket and has this id.
		if (ssrid != "") {
			respattrs["openapi.responder.release"] = sid
		}
		respbody = map[string]interface{}{"greeted": greetednames(), "total": totalgreeted}
		send(respattrs, respbody)
	default:
		respattrs["message.response.error"] = map[string]interface{}{"message":"Unexpected operation ID " + opid, "name":"Error"}
		send(respattrs, respbody)
	}
}
```

```javascript
// This file was generated by the OpenAPI Client Operator Generator

// Override this method to customize how the input message is read and the operation is selected

$.setPortCallback("input",onInput);

var id;

// Generated code
function isByteArray(data) {
  return (typeof data === 'object' && Array.isArray(data)
      && data.length > 0 && typeof data[0] === 'number')
}

function decode(s) {
   try {
     return JSON.parse(s);
   } catch(err) {
     return false;
   }
}

function onInput(ctx,s) {
  var msg = {};
  var inbody = s.Body;
  var inattributes = s.Attributes;

  // convert the body into string if it is bytes
  if (isByteArray(inbody)) {
    inbody = String.fromCharCode.apply(null, inbody);
  }
  
  if (typeof inbody === 'string' && inbody.indexOf('{') === 0) {
    input = decode(inbody);
  } else {
    input = inbody;
  }

  if (input != 'undefined' && input.operation){
    var msg = {};
    msg.Attributes = {};
    // add x-requested-with header to pass the vsystem's csrf check
    msg.Attributes["openapi.header_params.x-requested-with"] = "XMLHttpRequest";

    switch (input.operation) {
      
      case 'echo':
        echo(input, msg);
        break;
      
      case 'getGreetStatus':
        getGreetStatus(input, msg);
        break;
      
      case 'getGreetSummary':
        getGreetSummary(input, msg);
        break;
      
      case 'greet':
        greet(input, msg);
        break;
      
      case 'ping':
        ping(input, msg);
        break;
      
      case 'upload':
        upload(input, msg);
        break;
      
    }
    var msgid = inattributes["message.request.id"];
    if (msgid == undefined) {
        msgid = "request-" + id;
    }
    msg.Attributes["message.request.id"] = msgid;
    
    id++;

    $.output(msg);
  }
}


// Example payload to call this operation:
// {"operation":"echo","body":"string"}
function echo(input, msg) {
    // verify the required parameter 'body' is set
    if (input['body'] == undefined || input['body'] == null) {
        throw new Error("Missing the required parameter body when calling echo");
    }
    
    msg.Body = input.body;
    
    msg.Attributes["openapi.consumes"] = "text/plain";
    msg.Attributes["openapi.produces"] = "application/json";
    msg.Attributes["openapi.method"] = "POST";
    msg.Attributes["openapi.path_pattern"] = "/v1/echo";
}


// Example payload to call this operation:
// {"operation":"getGreetStatus","name":"string"}
function getGreetStatus(input, msg) {
    // verify the required parameter 'name' is set
    if (input['name'] == undefined || input['name'] == null) {
        throw new Error("Missing the required parameter name when calling getGreetStatus");
    }
    
    // path param name
    msg.Attributes['openapi.path_params.name'] =  input['name'] ;
    
    msg.Attributes["openapi.consumes"] = "";
    msg.Attributes["openapi.produces"] = "application/json";
    msg.Attributes["openapi.method"] = "GET";
    msg.Attributes["openapi.path_pattern"] = "/v1/greet/{name}";
}


// Example payload to call this operation:
// {"operation":"getGreetSummary"}
function getGreetSummary(input, msg) {
    msg.Attributes["openapi.consumes"] = "";
    msg.Attributes["openapi.produces"] = "application/json";
    msg.Attributes["openapi.method"] = "GET";
    msg.Attributes["openapi.path_pattern"] = "/v1/greet";
}


// Example payload to call this operation:
// {"operation":"greet","name":"string","body":{"name": "string","text": "string"}}
function greet(input, msg) {
    // verify the required parameter 'body' is set
    if (input['body'] == undefined || input['body'] == null) {
        throw new Error("Missing the required parameter body when calling greet");
    }
    
    msg.Body = input.body;
    
    // verify the required parameter 'name' is set
    if (input['name'] == undefined || input['name'] == null) {
        throw new Error("Missing the required parameter name when calling greet");
    }
    
    // path param name
    msg.Attributes['openapi.path_params.name'] =  input['name'] ;
    
    msg.Attributes["openapi.consumes"] = "application/json";
    msg.Attributes["openapi.produces"] = "application/json";
    msg.Attributes["openapi.method"] = "POST";
    msg.Attributes["openapi.path_pattern"] = "/v1/greet/{name}";
}


// Example payload to call this operation:
// {"operation":"ping"}
function ping(input, msg) {
    msg.Attributes["openapi.consumes"] = "";
    msg.Attributes["openapi.produces"] = "application/json";
    msg.Attributes["openapi.method"] = "GET";
    msg.Attributes["openapi.path_pattern"] = "/v1/ping";
}


// Example payload to call this operation:
// {"operation":"upload","name":"string","file":"path/to/file"}
function upload(input, msg) {
    if (input['file']) { 
        // file param file
        msg.Attributes['openapi.file_params.file'] = input['file'];
        msg.Attributes['openapi.file_params.file#name'] = input['file#name'];
    
    } 

    // verify the required parameter 'name' is set
    if (input['name'] == undefined || input['name'] == null) {
        throw new Error("Missing the required parameter name when calling upload");
    }
    
    // path param name
    msg.Attributes['openapi.path_params.name'] =  input['name'] ;
    
    msg.Attributes["openapi.consumes"] = "multipart/form-data";
    msg.Attributes["openapi.produces"] = "application/json";
    msg.Attributes["openapi.method"] = "POST";
    msg.Attributes["openapi.path_pattern"] = "/v1/greet/{name}/upload";
}
```

