JavaScript Operator
===============
com.sap.system.jsoperator<br>

Input<br>
--None--<br>
Output<br>
--None--<br>

JavaScript Operator를 사용하면 Graph내에서 JavaScript를 실행할 수 있습니다.

Configuration parameters
------------

* **codelanguage**: The programming language used in the snippet. ID: `codelanguage` | Type: `string` | Default: `"javascript"`
* **script** (mandatory): The inline script to be executed. If the script starts with "file://" then the script file is executed. ID: `script` | Type: `string` | Default: `""`

Input
------------
* **None**

Output
------------
* **None**

Creating a JavaScript extension
-----
1. JavaScript 연산자의 확장을 만들고 원하는 입력 및 출력 포트를 추가합니다.
2. 확장 구성에서 JavaScript 스니펫을 인라인 "스크립트" 매개변수로 추가하거나 코드를 별도의 파일에 넣고 `file://` 접두사를 사용하여 파일 이름을 지정합니다.

확장 프로그램을 만들려면 다음 단계를 따르세요.

1. Modeler UI에서 `Operators` 탭으로 이동하여 `+` 버튼을 클릭하여 새 연산자 확장을 추가합니다.
2. 기본 연산자 `Javascript Operator`를 선택하고 이름을 지정한 다음 `OK`을 클릭합니다.
3. 원하는 입력 및 출력 포트를 추가합니다.
4. JS 스크립트를 다음과 같이 추가하십시오.
   1. 확장 구성의 인라인 `script` 매개변수.
   2. 별도의 파일로 `file://` 접두사를 사용하여 `script` 매개변수에 파일 이름을 지정합니다.
5. 확장된 연산자를 저장합니다.

Basic example
-----
다음 예는 `input` port에서 들어오는 모든 메시지를 계산하고 그 수를 `output` port로 출력합니다.
```javascript
var counter = 0

$.setPortCallback("input",onInput)

function onInput(ctx,s) {
    counter++
    $.output(counter)
}
```

Generators
-----
Generator는 이벤트 처리 루프가 시작되기 전에 실행될 함수입니다.

다음 예는 `output` port에 `0`, `1`, `2`, `3`, `4`, `5` 값을 생성합니다.
```javascript
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
-----
Timer는 지정된 간격으로 호출됩니다. Timer는 선점형이 아닙니다. 따라서 주어진 간격은 Timer 기능이 호출될 간격의 하한선만 제공합니다. 모든 Timer는 **shutdown handlers**를 실행하기 전에 중지됩니다.

다음 예는 Graph가 종료될 때까지 `output` port에 `0`, `1`, `2`, ... 값을 출력합니다.
```javascript
var counter = 0

$.addTimer("1s",t1)

function t1(ctx) {
  $.output(counter)
  counter++
}
```
`addTimer()` 함수는 `removeTimer()` 함수를 통해 나중에 비활성화하는 데 사용할 수 있는 핸들러를 반환합니다.

다음 예에서 함수 `t1()`은 3번 호출됩니다. 그 후에 타이머가 제거되고 `t1()`이 더 이상 호출되지 않습니다.
```javascript
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
-----
메시지를 수정하려면 먼저 복사해야 합니다. 이를 위해 helper 함수인 `CopyMessage`가 제공됩니다. 메시지와 해당 속성의 shallow 복사만 수행합니다. 추가로 변경된 값은 별도로 복사해야 합니다.

연산자에 `in`과 `in2`라는 2개의 입력 포트와 `out`이라는 출력 포트가 있다고 가정하고 둘 다 `message` 유형입니다.
```javascript
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
-----
Shutdown handler는 이벤트 처리 루프 실행 후에 실행될 함수입니다.

다음 예제는 그래프가 종료 상태에 도달하면 2개의 값을 출력합니다. 각 값은 `input` 포트에서 수신된 입력 수를 나타냅니다.

예: 연산자가 7개의 입력을 받은 경우 그래프가 종료되면 `7`과 `7`을 출력합니다.
```javascript
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
-----
Configuration API는 graph 설명을 통해 제공된 operator configuration value를 읽을 수 있는 기능을 제공합니다.

다음 예에서는 **Generator function**를 사용하여 operator configuration인 `myStr`, `myInt`, `myBool`의 value를 읽습니다.
```javascript
function gen(ctx) {
  $.str($.config.getString("myStr"))
  $.int($.config.getInt("myInt"))
  $.bool(""+$.config.getBool("myBool"))
}
$.addGenerator(gen)
```

Graph termination
-----
`done` 함수를 사용하여 이 연산자가 실행을 완료했음을 알릴 수 있습니다. 이렇게 하면 다른 연산자가 성공적으로 실행을 완료한 경우 그래프가 `completed`으로 전환됩니다.

`fail` 함수는 그래프의 상태를 `dead`로 설정하는 오류를 발생시킵니다. `fail`로 제공된 메시지는 64,000자 이후에 잘립니다.

아래 예제는 입력 값이 짝수이면 연산자를 종료하고 그렇지 않으면 오류를 발생시킵니다.
```javascript
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
-----
다중성 관련 정보를 제공하는 두 가지 기능이 있습니다.

* `$.getMultiplicity()`: 연산자 그룹의 다중도를 반환합니다.
* `$.getMultiplicityIndex()`: 이 연산자의 여러 인스턴스를 구별하는 데 사용할 수 있는 [0,`$.getMultiplicity()`) 범위의 정수를 반환합니다.

Send message to logging app
-----
로그 함수를 통해 사용자는 Data Intelligence Logging app에 메시지를 보낼 수 있습니다. 이 기능의 매개변수는 `message`, `severity`, `messageCode`, `details` 입니다. `severity` 매개변수는 선택 사항이며 다음 열거형의 값 중 하나를 사용합니다.

* logSeverity.ERROR
* logSeverity.INFO
* logSeverity.WARNING

`messageCode` 및 `details` 매개변수도 선택사항입니다.

함수는 로깅 API 호출이 완료되기를 기다립니다. 클라이언트는 클라이언트 통신에 대해 10초 제한 시간으로 설정됩니다. 오류가 발생하거나 시간 초과에 도달하면 함수에 매개변수로 전달된 것과 동일한 severity와 함께 로그 메시지가 추적 프로그램에 기록됩니다. 다른 오류는 그래프를 죽입니다. Log API는 강력한 보증을 제공해야 합니다.

이 예제는 INFO severity가 있는 message, messageCode value, details 매개변수를 로깅 앱에 보냅니다.
```javascript
$.log("message to log", $.logSeverity.INFO, "10003", "this is a detailed message to the log message");
```

Subgraph (call a graph from js operator)
-----
`instanceiateGraph` 함수는 JavaScript 연산자에서 그래프를 호출할 수 있는 가능성을 제공합니다. 그래프에 대한 매개변수와 출력 포트에 대한 핸들러를 제공할 수 있습니다. `instanceiateGraph`는 그래프가 시작되거나 스크립트 실행이 실패할 때 그래프 객체를 반환합니다. 그래프 개체에는 다음과 같은 메서드가 있습니다.
- `wait` - 하위 그래프 실행이 완료될 때까지 스크립트 실행을 차단합니다. `wait`는 그래프 상태를 반환합니다.
- `stop` - 하위 그래프 종료를 시작합니다. 그래프 종료가 완료될 때까지 기다리지 않고 반환합니다.
```javascript
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
