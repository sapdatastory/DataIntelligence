`Python3` Operator
========

Python3 연산자를 사용할 때 `api` 객체가 제공하는 몇 가지 편의 기능을 제공하는 스크립트를 정의할 수 있습니다. 예를 들어 `api.set_port_callback("datain", callback_name)`을 작성하여 "datain" 포트에 새 데이터를 수신할 때 호출되는 콜백을 설정할 수 있습니다.

Python3 연산자를 확장하는 연산자는 Modeler의 **Repository** 탭에서 직접 생성할 수 있습니다.

> 이 연산자는 Python 3.6에서 실행됩니다.

Configuration Parameters
------------

* **script** (mandatory): 실행할 인라인 스크립트. 스크립트가 "file://"로 시작하면 스크립트 파일이 실행됩니다.  
  ID: `script` | Type: `string` | Default: `""`
  
* **Error handling** (mandatory): 연산자가 `prestart`, `port callback` 및 `timer callback` 중에 예외를 처리하는 방법을 정의합니다. `shutdown` 동안 예외가 이전에 트리거되지 않은 경우 그래프를 종료합니다. `Error Handling` 섹션에서 자세한 내용을 확인하세요.  
  ID: `errorHandling` | Type: `string` | Default: `"terminate on error"`
  
  Accepted values:

  * *terminate on error*: 예외는 그래프를 종료합니다.
  * *log and ignore*: 예외가 기록되고 연산자는 계속 실행됩니다.
  * *propagate to error port*: 예외는 error 포트로 전송되고 연산자는 계속 실행됩니다. `structure` 및 `com.sap.error` 유형의 `error`라는 포트가 생성되었다고 가정합니다.
    `code`, `text`, `details`와 같은 자세한 정보를 제공하기 위해 `OperatorException`이라는 사용자 정의 예외를 생성할 수 있습니다.
  * *retry*: 예외는 응답 콜백을 통해 전달됩니다. `Error Handling` 섹션에서 자세한 내용을 확인하세요.

Input
------------
* **None**

Output
------------
* **None**

Basic Examples
------
이 snipphet은 이름이 "input"이고 유형(scalar, "com.sap.core.int64")인 포트에서 들어오는 모든 message를 계산하고 "output"이라는 포트와 유형(scalar, "com.sap.core.int64")에 개수를 씁니다.

```python
counter = 0

def on_input(msg_id, header, data):
    global counter
    counter += 1
    api.outputs.output.publish(counter)

api.set_port_callback("input", on_input)
```

위 스크립트를 포함하는 연산자의 포트 "output"은 변수 `counter`가 파이썬 유형 `int`이기 때문에 `com.sap.core.int*` 유형이어야 합니다. 포트 유형을 선택하는 방법에 대한 자세한 내용은 `Correspondence between Core Scalars and Python types` 섹션을 참조하세요.

api.outputs.`port`.publish(data, header=None, response_callback=None)
----------------------------------------
    `data`와 `header`를 `port`라는 이름의 outport에 게시합니다.

> 연산자 초기화 후에만 출력이 가능합니다. 따라서 prestart, timer, callback 중에만.

    Args:
        data (...): Data to be sent.
        header (Header|dict, optional): dictionary mapping `header name`->[`header content`]. `Header` type, from port callbacks can also be used. If no header is provided, an empty header is used as default.
        response_callback(func[msg_id, ex], optional): Callback called after the message gets correctly received and processed by the next operator. `msg_id` identifies the message and matches the return from the publish functions. `ex` is an exception if there was one or `None`. `ex` comes from the message processing done by the next operator. If no `response_callback` is provided, the default function checks if `ex` is not None and raises an Exception if so.
    Returns:
        msg_id (bytes): 12 bytes message unique identifier in `port` specific connection.

Example:
```python
# Instead of raising an exception like the default, this custom only logs
def custom_response_callback(msg_id, ex):
    if ex:
        api.logger.error("Error when publishing %s: %s" % (str(msg_id), str(ex)))

def on_input(msg_id, header, body):

    # Access fields as dictionary
    header_val = header['header']

    # Read body value when not stream
    body_val = body.get()

    # Body cannot be directly sent, use the value instead
    # Header can be directly sent, it also possible copy (.copy())
    api.outputs.output.publish(body_val, header)
    
    new_header = {'new_header': ['example value']}

    # Also possible to send new header and body and response callback
    # Body should match the port type
    api.outputs.output.publish('example body', new_header, custom_response_callback)

api.set_port_callback("input", on_input)
```

api.outputs.`port`.publish(binary_data, n, header=None, response_callback=None)
----------------------------------------
    `data`(파일 객체로 가정)와 `header`의 첫 번째 `n` 바이트를 `port`라는 이름의 outport에 게시합니다. `n`이 -1이면 병렬 스트림 연결이 생성되고 이를 통해 데이터가 전송됩니다.

> 출력은 오퍼레이터 초기화 후에만 가능합니다. 따라서 prestart, timer, port callback 중에만.

    Args:
        data (...): file object, for example io.BytesIO.
        n (int): number of bytes to send. If `-1` is passed, all bytes are sent through a different stream connection. This can create overhead, so it is not recommended for small binary chunks. 
        header (Header|dict, optional): same as default publish.
        response_callback(func[msg_id, ex], optional): same as default publish.
    Returns:
        msg_id (bytes): 12 bytes message unique identifier in `port` specific connection.

Example:
```python
# Instead of raising an exception like the default, this custom only logs
def custom_response_callback(msg_id, ex):
    if ex:
        api.logger.error("Error when publishing %s: %s" % (str(msg_id), str(ex)))

def on_input(msg_id, header, body):

    # Read body value when stream
    body_reader = body.get_reader()
    value = body_reader.read(-1)
 
    # Send first 5 bytes of value, if there is less, all data is 
    # sent.
    msg_id = api.outputs.output.publish(BytesIO(value), 5)

    body = b'foo bar baz'
    # It is also possible to send at once, but it expects a file object
    # In this case we use BytesIO
    msg_id = api.outputs.output.publish(BytesIO(body), -1)

api.set_port_callback("input", on_input, {}, custom_response_callback)
```

api.outputs.`port`.with_writer(header=None, response_callback=None)
---------------------------------------
    `port`라는 이름으로 출력할 stream writer를 만듭니다.
    동적 포트의 경우 api.outputs.port.set_dynamic_type을 미리 호출해야 합니다. 자세한 내용은 "Working with Dynamic Types" 섹션을 참조하십시오.

> 출력은 오퍼레이터 초기화 후에만 가능합니다. 따라서 prestart, timer, port callback 중에만.

    Args:
        header (Header|dict, optional): dictionary mapping `header name`->[`header content`]. `Header` type, from port callbacks can also be used. If no header is provided, an empty header is used as default.
        response_callback(func[msg_id, ex], optional): Callback called after the message gets correctly received and processed by the next operator. `msg_id` identifies the message. `ex` is an exception if there was one or `None`. If no function is provided the default function checks if `ex` is not None and raises an Exception if so.
    Returns:
        msg_id (bytes): 12 bytes message unique identifier in `port` specific connection.
        writer (TableWriter|BinaryWriter): Object with a stream connection open to the next operator.
Example:
```python
# Assuming operator with input and output of com.sap.core.binary type
def on_input(msg_id, header, body):

    # Read body value when stream
    body_reader = body.get_reader()
    value = body_reader.read(-1)
 
    # Create stream writer
    msg_id, writer = api.outputs.output.with_writer()
    body = b'foo bar baz'
    writer.write(body)
    # Signals end of message
    writer.close()

    # It is also possible to send at once, but it expects a file-object
    # In this case we use BytesIO
    msg_id = api.outputs.output.publish(BytesIO(body), -1)

api.set_port_callback("input", on_input)

```

api.outputs.`port`.publish(None, header=headers, response_callback=None)
----------------------------------------
    header만 포함하고 body 데이터는 포함하지 않는 `none` 유형을 `port`라는 이름의 outport에 게시합니다.

> 출력은 오퍼레이터 초기화 후에만 가능합니다. 따라서 prestart, timer, port callback 중에만.

    Args:
        None: Used to signal the empty body, as the `none` type does not have data.
        header (Header|dict): dictionary mapping `header name`->[`header content`]. `Header` type, from port callbacks can also be used. If no header is provided, an empty header is used as default.
        response_callback(func[msg_id, ex], optional): Callback called after the message gets correctly received and processed by the next operator. `msg_id` identifies the message and matches the return from the publish functions. `ex` is an exception if there was one or `None`. `ex` comes from the message processing done by the next operator. If no `response_callback` is provided, the default function checks if `ex` is not None and raises an exception if so.
    Returns:
        msg_id (bytes): 12 bytes message unique identifier in `port` specific connection.

Example:
```python

def on_input(msg_id, header, body):

    # Access fields as dictionary
    header_val = header['header']

    # Header can be directly sent to the next operator, copy (.copy()) is also possible
    api.outputs.output.publish(None, header)
    
    new_header = {'new_header': ['example value']}

    # Also possible to send new header
    api.outputs.output.publish(None, new_header, None)

api.set_port_callback("input", on_input)
```

api.outputs.`port`.set_dynamic_type(dynamic_type)
---------------------------------------
    Associates the dynamic_type received to the publisher. This function should be called before `with_writer` when using a dynamic port.
    It will result in an exception if the port is statically typed. 

    Args:
        dynamic_type (api.DataTypeReference): dynamic type to be associated with the current publisher
    Returns:
        None

예를 들어 "Working with dynamic types" 섹션을 참조하세요.
    
Port Callbacks
--------------
#### api.set_port_callback(port, callback)
    Associate input `port` to the `callback`. The `callback` is called only when there is
    a message available in `port`.

    Args:
        port (str): input port to be associated with the callback. 
        callback (func[msg_id, header, body]): Callback called for each new message sent to `port`. `msg_id` identifies the message. For `header` and `body`, check `Header` and `InputBody` at `Data Types` section.

Prestart
--------
#### api.set_prestart(callback)
    Set a `callback` function to be executed before the event processing loop starts.

    Args:
        callback (func[None]): Callback executed before any port and timer callbacks are executed.
Example:

```python
counter = 0

# The same as the default response callback
def response_callback(msg_id, ex):
    if ex:
        raise ex

def prestart_function():
    global counter
    for i in range(0, 3):
        api.outputs.output.publish(counter, response_callback=response_callback)
        counter += 1

api.set_prestart(prestart_function)
```
이 예는 출력 포트 "output"에서 0,1,2 값을 생성합니다.

Timers
------
#### api.add_timer(callback)
    Multiple distinct periodic callbacks can be added. Timers are not preemptive. Thus, a set interval only provides the lower bound of the interval at which the timer function is called.

    Args:
        callback (func[None]->float): Callback function to be called. The following call interval is the return in `seconds`. If the return is `0`, the next call is made as fast as possible. If negative, the timer stops. 

Example:
```python
counter = 0

def t1():
    global counter
    api.outputs.output.publish({}, counter)
    counter += 1
    return counter

def response_callback(msg_id, ex):
    if ex:
        raise ex

api.set_response_callback("output", response_callback)

api.add_timer(t1)
```
이 예는 그래프가 종료될 때까지 0,1,2...초마다 포트 "output"에서 0,1,2... 값을 생성합니다.


Shutdown
--------
#### api.set_shutdown(callback)
    Set a `callback` function to be executed after the operator's stop event.

    Args:
        callback (func[None]): Callback executed after stopping the operator.

Example:
```python
counter = 0

def on_input(msg_id, header, body):
    global counter
    counter += 1

api.set_port_callback("input", on_input)

def shutdown():
    print("shutdown: %d" % counter)

api.set_shutdown(shutdown)
```

Configuration API
------
`api` 객체는 연산자의 편집기 view에 정의되거나 그래프 view의 구성 패널에 추가된 구성을 읽을 수 있는 가능성을 제공합니다. "foo"라는 이름의 구성을 정의했다면 `api.config.foo`를 호출하여 액세스할 수 있습니다. 구성 필드 이름에는 공백이 포함될 수 없습니다. "script" 및 "codelanguage" 구성 필드는 필수 구성 매개변수이므로 사용해서는 안 되므로 `api.config`에 표시되지 않습니다.
Modeler에서 config 필드를 JSON 객체로 채운 경우 해당 값은 dictionary(Python에서)가 됩니다.

> 이 연산자는 Modeler UI의 구성 탭에 포함된 추가 구성을 지원하지 않습니다. 그러나 구성은 `errorHandling` 및 `codelanguage`와 유사하게 그래프 JSON에 직접 포함될 수 있습니다.

Logging
-------
message를 기록하려면 `api.logger.info("some text")`, `api.logger.debug("")`, `api.logger.warn("")` 또는 `api.logger.error("")`를 사용하세요.

App Logging
-----------
> 이러한 함수를 호출할 때마다 HTTP 요청이 발생합니다. 이는 성능에 영향을 줄 수 있습니다.
#### api.app_log_error(message_code, message, details)
    Log error into Process Logs.

    Args:
        message code (str): Include a response code, such as 200, 404, FA1001.
        message (str): Main log message.
        details (str): Log more information about the event.

#### api.app_log_info(message_code, message, details)
    Log messages using `info` severity level.
#### api.app_log_warning(message_code, message, details)
    Log messages using `warning` severity level.

Error Handling
-----

4개의 `error handling` 옵션이 주어지면 `propagate to error port`만 연산자 스크립트에서 추가 지원이 필요합니다.
이 옵션은 [Error Message format](./service/v1/parse/readme/general/docu/errors/README.md)에 따라 '오류' 포트로 메시지를 트리거합니다.
연산자는 `api.OperatorException`을 발생시켜 `code`, `text` 및 `details`의 사용자 정의를 허용합니다.
이 예외 유형이 사용되지 않으면 `com.sap.error` 메시지의 기본값은 `0`인 `code`, `예외 메시지`인 `text`, 비어 있는 `details`입니다.

#### api.OperatorException(code, text, details)
    `propagate to error port`가 사용 중일 때 `com.sap.error` 메시지를 사용자 정의하기 위한 예외입니다.
  
        Args:
            code (int): error code specific to the operator. 
            text (str): string corresponding to the main error message.
            details (api.Table): table with two columns `key` and `value`, each of them strings.

Example:
```python
# Instead of raising an exception like the default, this custom only logs
# This function is called for all messages, but ex will contain an exception only if `retry` is set.
def custom_response_callback(msg_id, ex):
    if ex:
        api.logger.error("Error when publishing %s: %s" % (str(msg_id), str(ex)))

def on_input(msg_id, header, body):
    try:
        # Read body value when not stream
        body_val = body.get()
    except Exception as e:
        code = 1
        text = str(e)
        details = api.Table([['key', 'value']])
        # If `error_handling` is set to `propagate to error port` this exception will set the fields in the `com.sap.error` message. 
        raise api.OperatorException(code, text, details)

api.set_port_callback("input", on_input)
```

일반적으로 스크립트 내에서 모든 예외를 발생시키고 `error handling` 구성에 따라 처리하도록 할 수 있습니다.

예외가 연산자를 중지하도록 하려면 스크립트에서 `api.propagate_exception(e)`을 사용합니다. 여기서 e는 예외입니다.
참고: 스크립트의 기본 스레드(기본 스레드는 콜백을 실행하는 스레드)와 다른 스레드 내부에서 예외가 발생하는 경우 이전에 언급한 오류 처리 구성이 작동하지 않습니다. 결과적으로 스크립트는 `api.propagate_exception(e)`을 사용하거나 기본 스레드에 예외를 보내는 데 의존해야 합니다.

Halting Execution
-----------------

오류로 인해 그래프 실행을 중지하려면 **Error handling** 섹션의 지침을 따르세요.
오류 없이 그래프를 중지하기 위해 **Python Operator**는 **Graph Terminator Operator**에 신호를 보낼 수 있습니다.


Python 명령 `sys.exit(code)`를 사용하면 현재 Python 스레드만 종료되므로 사용을 권장하지 않습니다.
또한 전체 Python 프로세스가 중단되고 전체 그래프가 오류와 함께 중지되는 Python 명령 `os._exit(code)`를 사용하지 않는 것이 좋습니다.
전체 그래프가 오류로 중지되도록 하려면 **Error handling** 섹션의 지침을 따르세요.

repo_root and subengine_root
----------------------------

각각 api.repo_root 및 api.subengine_root를 사용하여 repo_root 및 subengine_root 경로에 액세스할 수 있습니다.
`/vrep` 경로 아래의 파일이나 폴더에 액세스하는 것은 지원되지 않으며 이러한 경로를 계속 사용할 수는 있지만 권장하지 않습니다.

graph_name, graph_handle and group_id
-------------------------------------

api.graph_name, api.graph_handle 및 api.group_id를 사용하여 graph_name, graph_handle 및 group_id 값에 각각 액세스할 수 있습니다.

* graph_name - 저장된 그래프의 식별자. 예: com.sap.dataGenerator
* graph_handle - 그래프 인스턴스의 고유 식별자. Modeler에서는 런타임 핸들이라고 합니다.
* group_id - 연산자가 실행 중인 그룹의 고유 식별자입니다.

multiplicity, multiplicity_index
--------------------------------

multiplicity 관련 정보 api.multiplicity 및 api.multiplicity_index를 얻기 위해 두 개의 변수에 액세스할 수 있습니다.

* multiplicity - 운영자 그룹의 multiplicity.
* multiplicity_index - 이 연산자의 여러 인스턴스를 구별하는 데 사용할 수 있는 [0, multiplicity) 범위의 정수입니다.

Inports and Outports
----------

각각 `api.get_inport_names()` 및 `api.get_outport_names()` 메소드를 호출하여 
현재 오퍼레이터 인스턴스에 대한 입력 및 출력 포트의 이름을 가져올 수 있습니다.

포트 이름을 key로 하고 연결 여부를 나타내는 boolean 값을 값으로 가지는 `api.is_inport_connected` 및 
`api.is_outport_connected` dictionary을 사용하여 어떤 inport 또는 outport가 연결되어 있는지 확인할 수 있습니다.

Example:
```python
if api.is_outport_connected["outport1"]:
    r = do_some_expensive_calculation()
    api.outputs.output1.publish({}, r)
```

Data Types
------

파이프라인 엔진의 타이핑 시스템에서 데이터 유형은 유형과 ID로 지정됩니다. ID는 다음 세 가지 범주 중 하나에 속할 수 있습니다.

- `scalar`
- `structure`
- `table`

scalar는 Modeler의 타이핑 시스템의 가장 기본적인 유형입니다. structure는 명명되고 정렬된 필드 모음입니다. 각 필드는 scalar 유형입니다. 이 데이터 모음을 record라고 합니다. table은 많은 record의 모음이거나 더 정확하게는 record의 정렬된 목록입니다.

scalar 유형은 템플릿을 기반으로 합니다. 템플릿은 고정된 유형 정의 집합입니다.

데이터 유형 섹션의 모델러를 통해 새 데이터 유형을 생성할 수 있습니다. 현재는 사용자 정의 structure와 table만 정의할 수 있습니다.

아래 표에서 핵심 scalar, 유형 템플릿 및 Python 유형 간의 관계를 찾을 수 있습니다.

| Core Scalar                | Template     | Python type       | Observation                                               |
| -------------------------- | ------------ |   --------------- |-----------------------------------------------------------| 
| com.sap.core.binary	     | binary       | bytes             |                                                           | 
| com.sap.core.bool	         | bool         | bool              |                                                           | 
| com.sap.core.byte	         | uint8        | int               |                                                           | 
| com.sap.core.date	         | date         | datetime.date     |                                                           | 
| com.sap.core.decfloat16	 | decfloat16   | decimal.Decimal   |                                                           | 
| com.sap.core.decfloat16	 | decfloat16   | decimal.Decimal   |                                                           | 
| com.sap.core.float32	     | float32      | float             |                                                           | 
| com.sap.core.float64       | float64      | float             |                                                           | 
| com.sap.core.geometry      | geometry     | bytes             |                                                           | 
| com.sap.core.geometryewkb	 | geometryewkb | bytes             |                                                           | 
| com.sap.core.int16	     | int32        | int               |                                                           | 
| com.sap.core.int32	     | int64        | int               |                                                           | 
| com.sap.core.int64	     | int64        | int               |                                                           | 
| com.sap.core.int8	         | int8         | int               |                                                           | 
| com.sap.core.string	     | string       | str               |                                                           | 
| com.sap.core.time	         | time         | datetime.time     |Loss of precision. Can only represent up to microseconds.  | 
| com.sap.core.timestamp     | timestamp    | datetime.datetime |Loss of precision. Can only represent up to microseconds.  | 
| com.sap.core.uint8         | uint8        | int               |                                                           | 


> :arrows_counterclockwise: 현재 개발 중입니다. 아직 사용할 수 없습니다.

Modeler에서 `decimal`, `date`, `time` 및 `timestamp` 템플릿은 `string`으로 표시됩니다. 다음 유형 중 하나를 검색할 때 사용자의 편의를 위해 반환된 개체는 더 쉽게 조작할 수 있도록 상위 수준 클래스로 변환됩니다.

`.get_raw()`를 호출하여 객체의 원시 문자열 표현을 검색하는 것도 가능합니다.

Data Type Reference
-----

API는 데이터 유형을 참조하기 위해 `api.DataTypeReference` 클래스를 노출(expose)합니다. 단일 개체에 유형과 ID를 보관하는 데 사용할 수 있습니다.
#### api.DataTypeReference(type, ID)
    Args:
        type (str): "scalar", "structure" or "table"
        ID (str): ID from type

```python
int64_type = api.DataTypeReference("scalar", "com.sap.core.int64")
```


Type Context
-----

type context는 type이 존재하는지 확인하거나 새 dynamic type를 만드는 것과 같이 type system과 상호 작용하는 메서드에 대한 액세스를 제공합니다.
API의 속성인 `api.type_context`로 액세스할 수 있습니다.

#### api.type_context.create_new_table(columns, keys)
    Creates a new dynamic table containing the specified columns. For an example, please check the section "Working with Dynamic Types".

    Args:
        columns (dic[str|api.DataTypeReference]): Dictionary mapping column names to their types.
        keys (List[str]): List containing the name of the key columns.

    Returns:
        ref (api.DataTypeReference): Reference to created type.

Working with Dynamic Types 
-----

포트는 정적 또는 동적으로 유형이 지정될 수 있습니다. 정적 포트에는 고정 유형과 ID가 있는 반면 동적 포트는 고정 유형을 유지하지만 모든 유형 ID를 보내거나 받을 수 있습니다. 한 가지 예는 항상 테이블을 출력하지만 각 테이블은 다른 스키마를 가질 수 있는 동적 테이블 출력입니다. 동적 포트의 ID는 `*`입니다.

`with_writer` 인터페이스를 사용하여 스트림을 통해 데이터를 출력하기 위해 동적 포트를 사용할 때 먼저 `publisher.set_dynamic_type`을 호출하여 유형을 동적 포트에 연결해야 합니다.
`publish` 인터페이스를 사용할 때 데이터에 유형 정보가 포함되어 있지 않으면 엔진이 이를 유추하려고 시도합니다.

다음 예에서는 런타임에 새 테이블 유형을 만들고 작성자를 가져오기 전에 게시자에 연결합니다.
```python
def create_new_dynamic_table():    
    columns_definition = {
      "id": api.DataTypeReference("scalar", "com.sap.core.int64"),
      "name": api.DataTypeReference("scalar", "com.sap.core.string"),
      "mean": api.DataTypeReference("scalar", "com.sap.core.float64")
    }
    table_type_ref = api.type_context.create_new_table(
        columns = columns_definition,
        keys = ["id"])
    
    api.outputs.my_dynamic_port.set_dynamic_type(table_type_ref)
    
    _, writer = api.outputs.my_dynamic_port.with_writer()
    
    table = read_data() # fictional function
    writer.write(table[100:])
    writer.close()
    
api.set_prestart(create_dynamic_table)
```

다음 예에서는 열을 수동으로 정의하는 대신 엔진에서 추론하도록 하고 싶습니다.
```python
def create_dynamic_table():
    
    data = [
        [1, "Lorem ipsum"],
        [2, "dolor sit"],
        [3, "amet consectetur"]
        ]
        
    table = api.Table(data)
    type_ref = table.infer_dynamic_type()
    
    api.outputs.my_dynamic_port.set_dynamic_type(type_ref)
    
    msg_id, w = api.outputs.my_dynamic_port.with_writer()
    w.write(table)
    w.close()
    
api.set_prestart(create_dynamic_table)
```

Record
-----
레코드는 스칼라 또는 테이블의 컬렉션을 나타내는 반복 가능한 클래스입니다. 생성자는 `api.Record`에서 호출할 수 있습니다.

해당 요소는 인덱싱을 통해 액세스할 수 있습니다.

> :arrows_counterclockwise: 현재 개발 중입니다. 아직 사용할 수 없습니다.

다음과 같은 방법을 제공합니다.

#### record.get_field_names()
    Returns (List(str)): list with the names of the fields that compose the structure.

#### record.get_field_type_ids()
    Returns (List(str)): list with the type IDs of the fields that compose the structure.

다음 예에서 ID가 `my.simpleStructure`인 가상 테이블의 입력 포트 `input1`이 있는 연산자를 가정해 보겠습니다. 이 테이블에는 3개의 열이 있습니다.

| Field Name                      | Field type     | Field id          | 
| --------------------------      | ------------   |  ------------      |
| id	                          | scalar         | com.sap.core.int64|
| name	                          | scalar         | com.sap.core.string|
| salary	                      | scalar         | com.sap.core.float64|


예제 코드에서는 입력 포트에서 데이터를 읽고 먼저 인덱싱을 사용하여 필드에 액세스한 다음 이름 필드로 액세스합니다.

Example code:
```python
def my_callback(msg_id, header, input_body):
    simple_structure = input_body.get()
    # using index to access id
    my_id = simple_structure[0]
    # fictitious function
    process_data(my_id, salary)

api.set_port_callback("input1", my_callback)
```

Table
-----
테이블은 정렬된 행 모음을 나타내는 반복 가능한 클래스입니다. 생성자는 `api.Table`에서 호출할 수 있습니다.
해당 요소는 인덱싱을 통해 액세스할 수 있습니다.

테이블에는 연결된 유형이 있을 수 있습니다. 유형이 지정된 테이블을 가지려면 생성자에 원하는 유형을 전달하거나 `infer_dynamic_type`을 호출하여 이를 나타내는 새 동적 유형을 생성할 수 있습니다.

#### api.Table(data: List, type_id: str)
    Arguments:
      data (List): data to compose the table body. Excepts a List of rows, in other words, a list of lists.
      type_id (str, optional): ID from type to associate to it.

    Returns:
      new_table (api.Table): created api.Table

다음과 같은 방법을 제공합니다.

#### table.is_typed()
    Returns (bool): boolean representing if the table has a type associated to it or not.

#### table.get_type_refence()
    Returns (api.DataTypeReference): reference to type associated to table. If table is not typed, returns None.

#### table.infer_dynamic_type()
    Creates a new dynamic type to represent the table schema. The type of the columns is infered based on the inner data.
    After called the table will be typed.

    Check the section "Working with dynamic types" for an example.

    Returns:
      type_ref (api.DataTypeReference): reference to new infered type


> :arrows_counterclockwise: 현재 개발 중입니다. 아직 사용할 수 없습니다.

#### table.to_pandas()
    Returns (pandas.DataFrame): Dataframe converted from the body of the table object.

Header
------
첫 번째 수준에 `str`이 key로, `List` 또는 `api.Record`가 값으로 있어야 하는 읽기 전용 dictionary입니다.

헤더는 읽기 전용 structure이므로 수정하려면 `.copy()` 메서드를 호출하여 수신된 헤더의 `dict` 표현을 가져와야 합니다. 이렇게 하면 연산자가 동일한 헤더를 가리킬 수 있으므로 예기치 않은 변경이 방지됩니다.

Example:
```python
def on_input(msg_id, header, body):
    api.logger.info(header['header-key'])

    dic_header = header.copy()
    dic_header['header-key'] = ['new', 'values']
    # sending the modified `header` to the next operator
    api.outputs.output('mock body', dic_header)

    # can also send the received header directly
    api.outputs.output('mock body', header)
```


InputBody
---------
InputBody는 들어오는 데이터를 wrapping하는 클래스입니다. 메시지 ID 및 header와 함께 콜백에서 수신됩니다. 연결된 포트 유형에 따라 수신된 개체 또는 스트림에 직접 액세스할 수 있습니다.

#### body.get()
    Return the data object for the following types:
    - (scalar, *), * for any scalar except for the ones based on the "binary" template.
    - (structure, *)
    Returns: data. The type depends on the type and ID of the associated input port.
    - (none)
    Returns: None, as the `none` type has no body. 
    Note: if `get` is called for a unsupported type, such as a table, an exception will be thrown.


#### body.get_reader()
    Return a reader if the port type is of type:
    - (scalar, *), * for any scalar based on the "binary" template.
    - (table, *)
    Returns (Reader|TableReader): stream reader.
    Note: if `get_reader` is called for an unsupported type, such as a string, an exception is thrown.

#### body.is_stream()
    Returns (bool): flags wheter the body supports streamming.

#### body.get_type_id()
    Returns (string): type ID of the associated port.

#### body.get_base_type()
    Return the type of the data associated.
    Returns (string): "scalar", "structure", "table" or "none".

TableWriter
-----------
테이블 스트림에 작성할 개체입니다. 특히 테이블의 경우 테이블을 일괄 처리로 출력할 수 있습니다. 예를 들어 게시자의 게시 기능도 사용합니다.

다음과 같은 기능을 제공합니다.

#### writer.write(rows)
    Write a list of rows into the stream.
    Args:
        rows (List[List] | api.Table): Table object to be streamed.
    Returns:
        n (int): Number of successfully written rows.

#### writer.close()
    Close the stream connection.


TableReader
-----------
테이블 스트림에서 읽을 개체입니다. 작성자가 스트림을 닫은 경우 EOF 신호가 없습니다. 대신 빈 테이블이 있습니다.

#### reader.read(n=-1)
    Read a list of rows from the stream and returns it in the table format. This function is blocked from returning if less than the desired number of rows is available and the stream is still open. If the stream is closed, read can return less than `n` rows. If `-1` is passed, rows are read until writer closes the stream.
    Args:
        n (int): Number of rows to be read.
    Returns:
        table (api.Table): Table object containing the read rows.

> :arrows_counterclockwise: 현재 개발 중입니다. 아직 사용할 수 없습니다.
#### reader.read_dataframe(n=-1)
    Read a list of rows from the stream and returns it in the dataframe form. This function is blocked from returning if less than the desired number of rows is available and the stream is still open. If the stream is closed, read can return less than n rows. If -1 is passed, rows are read until writer closes the stream.
    Args:
        n (int): Number of rows to be read.
    Returns:
        df (pandas.DataFrame): dataframe object containing the read rows.

Example:
```python
def on_input(msg_id, header, body):
    api.logger.info(header['header-key'])
    
    table_reader = body.get_reader()
    table = table.read(5) # Read only first 5 rows as a table
    if len(table) < 5: # This means the stream is over
        api.logger.error("unexpected table length")

    # Create output writer and send only first 5 read rows
    msg_id, writer = api.outputs.output.with_writer(header)
    writer.writer(table)
    writer.close()
```

BinaryWriter
-----------
바이너리 스트림에 작성할 개체입니다. 바이트를 배치로 출력하는 것도 가능합니다. 예를 들어 게시 기능도 사용합니다.

#### writer.write(data: bytes)
    Write a bytes into the stream.
    Args:
        data (bytes): bytes to be streamed.
    Returns:
        n (int): Number of successfully written bytes.

#### writer.flush()
    Flush the stream connection.

#### writer.close()
    Close the stream connection.

BinaryReader
-----------
바이트 스트림에서 읽을 개체입니다. 0바이트가 반환되고 크기가 0이 아니면 스트림의 끝을 나타냅니다.

#### reader.read(n=-1)
    Read bytes from the stream. This function is blocked from returning if less than the desired number of bytes is available and the stream is still open. If the stream is closed, read can return less than n bytes. If -1 is passed, bytes are read until writer closes the stream.
    Args:
        n (int): Number of bytes to be read.
    Returns:
        data (bytes): bytes read.

Correspondence Type Templates, Python Types and dtypes
-----------------------------------------------------

테이블을 dataframe으로 읽을 때 필요한 경우 테이블의 개별 데이터 조각이 다른 형식으로 변환됩니다.

아래 표에서 테이블 형식에서 pandas dataframe으로 변환한 후 스칼라 유형의 요소에 대해 예상되는 dtype을 찾을 수 있습니다.

| type template | Python type | dtype          | Limitations                                                                               |
|---------------|-------------|----------------|-------------------------------------------------------------------------------------------|
| bool          | bool        | bool           |                                                                                           |
| int8          | int         | int64          |                                                                                           |
| int16         | int         | int64          |                                                                                           |
| int32         | int         | int64          |                                                                                           |
| int64         | int         | int64          |                                                                                           |
| uint64        | int         | uint64*        | *The smallest possible between uint8, uint16, uint32 and uint64 that can hold all values. |
| float32       | float       | float64        |                                                                                           |
| float64       | float       | float64        |                                                                                           |
| decimal       | str         | object*        |                                                                                           |
| date          | str         | datetime64[ns] | Can only represent range: 1677-09-21 - 2262-04-11                                         |
| time          | str         | datetime64[ns] |                                                                                           |
| timestamp     | str         | datetime64[ns] | Can only represent range: 1677-09-21 00:12:43.145225 - 2262-04-11 23:47:16.854775807      |
| string        | str         | object         |                                                                                           |
| geometry      | bytes       | object         |                                                                                           |
| geometryewkb  | bytes       | object         |                                                                                           |

null이 있는 경우 dataframe의 해당 값은 pd.NA 유형입니다(사용할 수 없음). null이 있는 경우 열에는 혼합 유형이 있고 열 dtype은 개체입니다.

State Management
----------------

> 이렇게 하려면 스냅샷이 활성화된 상태에서 그래프를 실행해야 합니다. 이는 그래프 런타임에 직접적인 영향을 주지만 복구를 제공합니다.

연산자가 상태 관리가 활성화된 상태에서 실행될 것으로 예상되고 내부 상태가 있는 경우에 사용해야 합니다. 이 연산자를 상태 저장이라고 합니다. 기본적으로 상태 저장이 아닌 모든 연산자는 아래 기능을 구현할 필요가 없습니다.
연산자 상태를 선언하려면 `set_initial_snapshot_info`를 호출할 때 옵션이 설정되어 있어야 합니다. 상태가 있는 경우 운영자는 최소한 `set_restore_callback` 및 `set_serialize_callback`을 구현해야 합니다.

상태 관리를 지원하는 연산자는 generator와 writer라는 두 가지 추가 클래스를 가질 수 있습니다. generator는 `api.OutportInfo`에서 자세히 설명합니다. writer는 그래프 외부에 영향을 미치는 연산자입니다. 예를 들어 연산자가 데이터베이스에 쓰거나 게시자 또는 구독자 대기열에 쓰는 경우입니다.
연산자가 작성자인 경우 상태 저장인 경우 최소 한 번 보증을 제공합니다. 즉, 두 번 쓸 수 있더라도 데이터가 손실되지 않는다는 보장이 있습니다. 상태를 저장하려면 복원 및 직렬화 기능을 구현해야 합니다.
정확히 한 번 보장하는 것도 가능합니다. 이렇게 하려면 작성자가 상태 저장 외에도 멱등성이 있어야 합니다. 멱등성(idempotency)은 같은 데이터를 여러 번 쓸 때 등가성(equivalency)을 의미합니다.

다음은 상태 관리와 연산자가 이를 지원할 수 있는 방법에 관한 몇 가지 일반적인 관찰입니다.
 - 포트 콜백은 다른 콜백을 기다리는 동안 차단되어서는 안 됩니다. 이로 인해 교착 상태가 발생합니다.
 - 상태를 저장하기 전에 종료 기능이 일시 중지되지 않습니다. 따라서 종료 기능은 운영자 상태를 변경하지 않아야 합니다.

다음 예제 스크립트는 상태 관리 기능 사용법을 보여줍니다. 자세한 내용은 뒤에 설명합니다.

```python


import pickle

acc = 0

def on_input(msg_id, header, body):
    global acc
    v = int(body.get())
    acc += v
    api.outputs.output.publish("%d" % (acc))

api.set_port_callback("input", on_input)

api.set_initial_snapshot_info(api.InitialProcessInfo(is_stateful=True))

def serialize(epoch):
    return pickle.dumps(acc)

api.set_serialize_callback(serialize)

def restore(epoch, state_bytes):
    global acc
    acc = pickle.loads(state_bytes)

api.set_restore_callback(restore)

def complete_callback(epoch):
    api.logger.info(f"epoch {epoch} is completed!!!")

api.set_epoch_complete_callback(complete_callback)
```

#### api.InitProcessInfo
    Class for initial state management information about the operator.

    Args:
        is_stateful (bool, optional): Whether the operator has a internal state to store. Default is false.
        outports_info (dict[str, api.OutportInfo], optional): A dictionary to configure the output ports. Default is a empty dictionary.

#### api.OutportInfo
    Class for operator output port information.

    Args:
        is_generator (bool, optional): A generator is a port that produces outputs independent of input ports data. All graphs which have data flowing have at least one generator output port. Examples of generators include operators reading files with no input connected or Kafka consumers.

#### api.set_initial_snapshot_info(initial_process_info)
    Set the initial information for State management before starting the operator. This should be called outside callback functions.

    Args:
        initial_operator_info (api.InitProcessInfo)

#### api.set_restore_callback(callback)
    Register function which restores the operator state.
  
    Args:
        callback (func[str, bytes] -> None]): The function should expect two input parameters. The first is the epoch, which uniquely identifies the state that is being recovered. The second is the serialized operator state.
    
#### api.set_serialize_callback(callback)
    Register function that returns the operator state.

    Args:
        callback (func[str] -> bytes): The function should expect the epoch as a parameter. Epoch uniquely identifies the state that is being recovered. It should return the serialized operator state.

일반적으로 상태 관리를 지원하는 연산자에게 내부 연산자 상태를 변경하거나 데이터를 출력 포트로 보낼 수 있는 새 스레드 또는 프로세스를 생성하는 것은 권장되지 않습니다. 이것을 피할 수 없다면 `set_pause_callback`과 `set_resume_callback`을 사용해야 합니다.
예를 들어 연산자가 입력 포트 콜백 내부에서 스레드를 시작하고 이 스레드가 출력 포트에 쓰는 경우입니다. 이를 위해서는 두 가지 기능을 구현해야 하며 `threading.Lock`에 의존할 수 있습니다. 일시 중지 콜백은 잠금을 획득할 수 있는 반면 재개 콜백은 잠금을 해제합니다.

#### api.set_pause_callback(None)
    This function needs to finish or pause all actions that can affect the internal operator state before it returns.

#### api.set_resume_callback(None)
    This function needs to recover all actions that were stopped when pausing the operator.

#### api.set_epoch_complete_callback(callback)
    Function called when all operators in a graph have saved their states. This means the state identified by the epoch sent as a parameter to this function is over.
    Args:
        callback (func[str] -> None): the epoch is passed as a parameter.

FAQ
---
#### 연산자의 초기화 코드는 어디에 배치해야 합니까?

스크립트는 한 번만 실행됩니다. 
스크립트에 정의된 콜백 함수는 여러 번 실행할 수 있지만 스크립트의 가장 바깥쪽 범위의 명령은 한 번만 실행됩니다. 
이는 스크립트 본문에 초기화 코드를 간단히 배치할 수 있음을 의미합니다. 
아래 예를 참조하십시오.

```python
# Hypothetical script for Python3Operator

# In the operator's initialization we might want to setup a connection
# with a database for example (`setup_connection` is an hypothetical function):
db = setup_connection(api.config.host, api.config.port)

def my_callback_func(data):
    global db
    db.write(data)  # hypothetical call

api.set_port_callback("input", my_callback_func)
```

또는 `api.set_prestart(func)`로 함수를 등록하여 prestart 함수에 초기화 코드를 넣을 수도 있습니다.

출력은 연산자 초기화 후에만 가능합니다. 따라서 prestart, timer, port callback 중에만.

