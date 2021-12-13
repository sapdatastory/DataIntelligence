Http Server/Client Operator 처리 예제
===

# 1. Http Server
## 1.1 Http Server Operator : message <-> message
![](images/1.FilePython.png)<br>
HTTP Server --> JS(3) --> 3:1 Multiplexer --> JS

Base Path : /samples/plain_greeter

```javascript
$.setPortCallback("request", function(ctx, msg) {
    $.command({
        Attributes: {
            "message.request.id": msg.Attributes["message.request.id"],
            "objectStore.command": "select",
            "objectStore.id": msg.Attributes["http.vars"]["id"]
        },
        Body: null
    });
});
```

```javascript
$.setPortCallback("request", function(ctx, msg) {
    $.command({
        Attributes: {
            "message.request.id": msg.Attributes["message.request.id"],
            "objectStore.command": "insert",
            "objectStore.id": msg.Attributes["http.vars"]["id"]
        },
        Body: msg.Body
    });
});
```

```javascript
$.setPortCallback("request", function(ctx, msg) {
    $.command({
        Attributes: {
            "message.request.id": msg.Attributes["message.request.id"],
            "objectStore.command": "delete",
            "objectStore.id": msg.Attributes["http.vars"]["id"]
        },
        Body: null
    });
});
```

```javascript
function isByteArray(data) {
    switch (Object.prototype.toString.call(data)) {
        case "[object Int8Array]":
        case "[object Uint8Array]":
            return true;
        case "[object Array]":
        case "[object GoArray]":
            return data.length > 0 && typeof data[0] === 'number';
    }
    return false;
}

var objects = {};
var commands = {
    "select": function(id, body) {
        if(!objects.hasOwnProperty(id))
            return "no object with ID " + id;
        return JSON.stringify(objects[id]);
    },
    "insert": function(id, json) {
        if(objects.hasOwnProperty(id)) {
            return "error: an object with ID " + id + " already exists";
        }
        if (isByteArray(json)) {
            json = String.fromCharCode.apply(null, json);
        }
        var o = JSON.parse(json);
        objects[id] = o;
        return "1 object inserted";
    },
    "delete": function(id, body) {
        if(!objects.hasOwnProperty(id)) {
            return "no object deleted";
        }
        delete objects[id];
        return "1 object deleted";
    }
};

$.setPortCallback("command", function(ctx, msg) {
    var cmd = msg.Attributes["objectStore.command"];
    var id = msg.Attributes["objectStore.id"];
    var result = commands[cmd](id, msg.Body);
    $.result({
        Attributes: {
            "message.request.id": msg.Attributes["message.request.id"]
        },
        Body: result
    });
});
```
