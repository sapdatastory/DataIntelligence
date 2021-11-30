# JavaScript Operator 사용 방법
JavaScript Operator를 사용하면 Graph내에서 JavaScript를 실행할 수 있습니다.

기본 예제
```shell
var counter = 0

$.setPortCallback("input",onInput)

function onInput(ctx,s) {
    counter++
    $.output(counter)
}
```

Generators
```shell
var counter = 0

$.addGenerator(gen)
$.addGenerator(gen)

function gen(ctx) {
    for (var i = 0; i < 3; i++ ) {
      $.output(counter)
      counter++
    }
}
```

Timers
```shell
var counter = 0

$.addTimer("1s",t1)

function t1(ctx) {
  $.output(counter)
  counter++
}
```
```shell
var counter = 0

var timerId = $.addTimer("100ms",t1)

function t1(ctx) {
    counter++
    console.log("in t1() counter == ", counter)
    $.output(counter)

        if (counter == 3)
        $.removeTimer(timerId)
}
```

Handling messages
```shell
$.setPortCallback("in", onIn)
$.setPortCallback("in2", onIn2)

function onIn(ctx,s) {
    // the message must be copied before modifying it
    var m = $.copyMessage(s);

    // modifying an attribute reference
    // no further copy needed
    m.Attributes["foo"] = "bar";

    // modifying the body's reference
    // no further copy needed
    m.Body = "my-new-body"

    $.out(m)
}

function onIn2(ctx,s) {
    // the message must be copied before modifying it
    var m = $.copyMessage(s);

    // modifying an attribute value
    // a copy is needed
    var oldFoo = m.Attributes["foo"];
    if (Array.isArray(oldFoo)) {
        var newFoo = oldFoo.slice() + "foo";
        m.Attributes["foo"] = newFoo;
    }

    // modifying the body's contents
    // a copy is needed
    // set the first value to 1
    var oldBody = m.Body;
    if (Array.isArray(oldBody)) {
        var newBody = oldBody.slice();
        newBody[0] = 0x01;
        m.Body = newBody;
    }

    $.out(m)
}
```

Shutdown handlers
```shell
var counter = 0

$.setPortCallback("input",onInput)

function onInput(ctx,s) {
    counter++
}

function shutdown(ctx) {
    $.output(counter)
}

$.addShutdownHandler(shutdown)
$.addShutdownHandler(shutdown)
```

Configuration API
```shell
function gen(ctx) {
  $.str($.config.getString("myStr"))
  $.int($.config.getInt("myInt"))
  $.bool(""+$.config.getBool("myBool"))
}
$.addGenerator(gen)
```

Graph termination
```shell
$.setPortCallback("input", onInput)

function onInput(ctx,s) {
    v = parseInt(s)
    if (v % 2 === 0) {
      $.done()
    } else {
      $.fail("unexpected value received")
    }
}
```

Handling multiplicity
$.getMultiplicity(): returns the multiplicity of the operator’s group.
$.getMultiplicityIndex(): returns an integer in the range

Send message to logging app
```shell
$.log("message to log", $.logSeverity.INFO, "10003", "this is a detailed message to the log message");
```

Subgraph (call a graph from js operator)
```shell
$.addGenerator(gen)

// This example shows basic usage of a subgraph
// It calls a graph with a parameter, provides input to a port,
// checks a port's output and stops the graph

var graphName = "com.sap.demo.subgraph.call-and-wait.sub"
var subgraphInput = "subgraph-input "
var paramValue = "value1"
function gen(ctx) {
  // start subgraph
  var g
  try {
    g = $.instantiateGraph(graphName,
      {"param1": paramValue},
      // handle subgraph output port with name 'output'
      {"output":function(ctx,s){
          // check subgraph output
          if (s != subgraphInput + paramValue) {
              $.fail("Unexpected subgraph output: " + s + " Expected: " + prefix+paramValue)
          }
          // stop subgraph
          g.stop()
      }}
    )
  } catch(e) {
    $.fail(e.message)
    return
  }
  // write string in subraph input port with name 'input'
  g.input(subgraphInput)
  // wait for graph execution is finished
  status = g.wait()
  // check graph status
  if (status != $.graphStatus.completed) {
    $.fail("Subgraph is failed")
  } else {
    $.done()
  }
}
```
