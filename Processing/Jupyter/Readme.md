Jupyter Operator
===============

Jupyter 연산자는 Python 3.6.x 코드를 사용하여 데이터 흐름과 상호 작용할 노트북을 만들 수 있는 Jupyter 노트북 애플리케이션을 시작합니다. 
Python 3 연산자(`com.sap.system.python3Operator`)와 유사하게 동작합니다.

연산자는 `interactive` 및 `productive` 두 가지 실행 모드를 제공합니다. interactiver 모드에서 Jupyter 노트북 UI에 액세스하여 데이터 스트림과 상호 작용할 수 있습니다. 
스크립트에 대해 원하는 동작이 있으면 Jupyter 연산자가 Python 3 연산자로 동작하고 셀을 실행하는 데 사용자 상호 작용이 필요하지 않은 productive 모드로 전환할 수 있습니다. 
`Running in Productive mode` 섹션에서 자세한 내용을 참조하십시오.

Modeler의 비동기 특성으로 인해 데이터 처리는 콜백으로 수행됩니다. 
예를 들어 `api.set_port_callback("in", callback_name)`을 호출하여 "in" 포트에 새 데이터가 수신될 때 호출되는 콜백을 설정할 수 있습니다. 
다른 미리 정의된 기능은 이 문서의 나머지 섹션에 설명되어 있습니다.

> 참고: 이 연산자는 python 3.6에서 실행됩니다.

Configuration parameters
------------

* **Notebook File Path** (mandatory): Path to the notebook to be created or to be opened from the file system or ML scenario. Note that new notebooks can be created only in the graph folder (this is, the file path should include only a file name). For notebooks that belong to an ML scenario, this operator needs to be in a pipeline created from the ML Scenario Manager and the path should be the file name of the notebook. To reference an existing path, use the absolute path from the file system. In this case, this value should likely be a path from vrep that starts with “/files”. If the referenced file does not exist, it results in the pipeline failing. ID: `notebookFilePath` | Type: `string` | Default: `""`

* **Productive** (mandatory): Flags whether the operator should run in productive mode or not.
ID: `Productive` | Type: `boolean` | Default: `false`

* **Timeout** (mandatory): The maximum number of seconds to wait for data at an input port.
ID: `Timeout` | Type: `integer` | Default: `5`


Input
------------
* **None**

Output
------------
* **None**

Interacting with the jupyter notebook UI
-----
interactive 모드에서는 Jupyter 노트북 UI에 액세스하여 셀을 실행하여 데이터 스트림과 상호 작용할 수 있습니다.

Jupyter 노트북 UI를 열려면 Modeler 캔버스에서 연산자를 마우스 오른쪽 버튼으로 클릭하고 "Open UI" 버튼을 클릭합니다. 노트북 인터페이스와 함께 새 탭이 열려야 합니다.

Examples
------
Writing data to an output port
------

"input" 포트에서 들어오는 모든 메시지를 계산하고 "output" 포트에 카운트를 씁니다.
```python
counter = 0

def on_input(data):
    global counter
    counter += 1
    api.send("output", counter)

api.set_port_callback("input", on_input)
```

위 스크립트를 포함하는 연산자의 "output" 포트는 'int64' 유형이어야 합니다. 변수 'counter'가 Python 유형 'int'이기 때문입니다. 포트 유형을 선택하는 방법에 대한 자세한 내용은 `Correspondence between Modeler types and python types`을 참조하세요.

`api.set_port_callback`은 핸들러를 호출하기 전에 두 개의 입력 포트가 데이터를 수신할 때까지 기다리는 데 사용할 수도 있습니다.

```python
def on_input(data1, data2):
    api.send("output", data1 + data2)

api.set_port_callback(["input1", "input2"], on_input)
```

api.send(port, data)
-------------------------
    'port'라는 이름의 outport에 'data'를 보냅니다.

    Args:
        port (str): Name of output port.
        data (...): Object to be sent.


Port callbacks
--------------
#### api.set_port_callback(ports, callback)
    이 메소드는 입력 `ports`를 `callback`에 연결합니다. 
    'callback'은 모든 'ports'에서 사용할 수 있는 메시지가 있을 때만 호출됩니다. 
    이 메소드가 동일한 포트 그룹에 대해 여러 번 호출되면 이전 'callback'이 새 'callback'으로 대체됩니다. 
    다른 포트 그룹은 겹칠 수 없습니다. 동일한 콜백 함수를 다른 포트 그룹에서 재사용할 수 없습니다.

    Args:
        ports (str|list[str]): input ports to be associated with the callback. `ports` can be a list of strings
                               with the name of each port to be associated or a string if you want to associate the
                               callback to a single port.
        callback (func[...]): a callback function with the same number of arguments as elements in `ports` or a variable length argument.
                              The arguments are passed to `callback` in the same order of their corresponding
                              ports in the`ports` list.

팁: 여러 포트 그룹에서 동일한 콜백 함수를 재사용하려는 경우 
관심 있는 함수를 반환하는 함수를 사용할 수 있습니다.
```
def get_my_callback():
  def my_callback(data):
      # some code here
  return my_callback

api.set_port_callback("inport1", get_my_callback())
api.set_port_callback("inport2", get_my_callback())
```
이렇게 하면 매번 다른 ID를 가진 새 함수가 생성되지만 
콜백 동작은 동일하게 유지됩니다.

#### api.remove_port_callback(callback)
    `callback` 기능을 등록 취소합니다. 존재하지 않으면 메서드가 조용히 종료됩니다.

    Args:
        callback: Callback function to be removed.

Generators
------
Generator는 이벤트 처리 루프가 시작되기 전에 실행되는 함수입니다. 추가된 순서대로 실행됩니다.
```python
counter = 0

def gen():
    global counter
    for i in range(0, 3):
        api.send("output", counter)
        counter += 1

api.add_generator(gen)
api.add_generator(gen)
```
이 예는 출력 포트 "output"에서 0,1,2,3,4,5 값을 생성합니다.

Timers
------
#### api.add_timer(period, callback)
    여러 개의 고유한 주기적 콜백을 추가할 수 있습니다. 이미 추가된 콜백이 다시 추가되면 이전 period가 새 'period'로 바뀝니다. 
    타이머는 선점형이 아닙니다. 따라서 주어진 간격은 타이머 함수가 호출되는 간격의 하한값만 제공합니다.
    'period'가 0이면 콜백이 최대한 빨리 호출된다는 의미입니다.
    
    동일한 동작을 가진 두 개의 콜백을 동시에 실행하려면 
    
    동일한 본문을 가진 두 개의 다른 함수를 생성하거나 내부 함수를 정의하고 반환하는 factory 함수를 생성해야 합니다. 
    factory 함수가 호출될 때마다 새로운 함수(다른 ID를 가진)가 반환되지만 동작은 동일합니다. 
    factory 함수의 예를 보려면 set_port_callback 섹션의 팁을 참조하세요.

    Args:
        callback (func): Callback function to be called every `milliseconds`.
        period (str): Period between calls of `callback`. It is passed as a string.
                      For example, "-1.3h3m2us" means minus (1.3 hours 3 minutes and 2 microseconds),
                      which is converted to: -(1.3*3600 + 3*60 + 2*1e-6) = -4860.000002 seconds.
                      Available suffixes are: h, m, s, ms, us, ns.
                      They represent hours, minutes, seconds, milliseconds, microseconds, and nanoseconds, respectively.
                      If the input uses multiple units, it needs to follow the same order presented in
                      the previous sentence. That is, "2h3s" is allowed, but "3s2h" is not.
                      Only strings "0", "+0", "-0" are allowed not to have a unit of time suffix
                      (they are optional in these cases). Signs are optional and are allowed just in the
                      beginning of the string.

Example:
```python
counter = 0

def t1():
    global counter
    api.send("output", counter)
    counter += 1

api.add_timer("1s", t1)
```
이 예는 그래프가 종료될 때까지 포트 "output"에서 0,1,2...값을 생성합니다.

#### api.remove_timer(callback)
    타이머 콜백 등록을 취소합니다.

    Args:
        callback (func): Callback function to be removed.

#### api.update_timer(period, callback)
    기존 'callback' period를 업데이트합니다.
    콜백이 존재하지 않으면 오류가 발생하지 않습니다.

    Args:
        callback (func): Callback function for which the period is updated. If `callback` is not registered,
                         nothing changes.
        period (str): String number representing a new period to overwrite the old value.

Shutdown handlers
------
Shutdown handler는 operator stop 이벤트 이후에 추가된 순서대로 실행되는 함수입니다.
```python
counter = 0

def on_input(data):
    global counter
    counter += 1

api.set_port_callback("input", on_input)

def shutdown1():
    print("shutdown1: %d" % counter)

def shutdown2():
    print("shutdown2: %d" % counter)

api.add_shutdown_handler(shutdown1)
api.add_shutdown_handler(shutdown2)
```
This example print "shutdown1: 7" and "shutdown2: 7" if 7 values are provided on "input" port.

Configuration API
------
`api` 객체는 연산자의 에디터 view에 정의되거나 그래프 view의 구성 패널에 추가된 구성을 읽을 수 있는 가능성을 제공합니다. 
"foo"라는 구성을 정의하면 `api.config.foo`를 호출하여 액세스할 수 있습니다. 구성 필드 이름에는 공백이 포함될 수 없습니다. 
"script" 및 "codelanguage" 구성 필드는 필수 구성 매개변수이므로 사용해서는 안 되므로 `api.config`에 표시되지 않습니다.
Modeler의 구성 필드에 json 객체를 추가하면 Python에서 dictionary가 됩니다.

Logging
-------
message를 기록하려면 `api.logger.info("some text")`, `api.logger.debug("")`, `api.logger.warn("")` 또는 `api.logger.error("")`를 사용하세요.

Error handling
-----
스크립트 내에서 모든 예외를 발생시킬 수 있습니다. 결과적으로 예외 메시지가 기록되고 연산자가 종료됩니다. 예외가 스크립트의 기본 스레드와 다른 스레드 내부에서 throw되는 경우는 예외입니다. 이 경우 `api.propagate_exception(e)`을 호출해야 합니다. 여기서 **e**는 예외 객체를 올바르게 처리하기 위한 예외 객체입니다.

> 참고: 의도하지 않은 결과를 초래할 수 있으므로 stderr에 쓰지 마십시오. 또한 `api.logger.fatal` 또는 `api.logger.critical`을 사용하지 마십시오. 그렇지 않으면 그래프가 중지됩니다. 그래프를 중지하고 

Halting execution
-----------------

오류로 인해 그래프 실행을 중지하려면 **Error handling** 섹션의 지침을 따르세요.
오류 없이 그래프를 중지하기 위해 **Python Operator**는 **Graph Terminator Operator**에 신호를 보낼 수 있습니다.

연산자의 실행만 중지해야 하는 경우(그래프 전체를 중지하지 않고) 모든 콜백을 등록 취소할 수 있습니다.
단일 연산자를 중지하면 그래프의 데이터 흐름이 전체적으로 중지될 수 있습니다.

참고: Python 명령 `sys.exit(code)`를 사용하면 현재 Python 스레드만 종료되므로 사용하지 않는 것이 좋습니다.
또한 Python 명령 `os._exit(code)`를 사용하지 않는 것이 좋습니다. 이 명령은 전체 Python 프로세스를 중단하고 그래프가 오류와 함께 중지되도록 합니다.
전체 그래프가 오류로 중지되도록 하려면 **Error handling** 섹션의 지침을 따르세요.

repo_root and subengine_root
----------------------------

각각 api.repo_root 및 api.subengine_root를 사용하여 repo_root 및 subengine_root 경로에 액세스할 수 있습니다.

graph_name, graph_handle and group_id
-------------------------------------

api.graph_name, api.graph_handle 및 api.group_id를 사용하여 graph_name, graph_handle 및 group_id 값에 각각 액세스할 수 있습니다.

* graph_name - 저장된 그래프의 식별자. 예: com.sap.dataGenerator
* graph_handle - 그래프 인스턴스의 고유 식별자. 모델러 사용자 인터페이스에서는 런타임 핸들이라고 합니다.
* group_id - operator가 실행 중인 그룹의 고유 식별자

multiplicity, multiplicity_index
--------------------------------

multiplicity 관련 정보 api.multiplicity 및 api.multiplicity_index를 얻기 위해 두 개의 변수에 액세스할 수 있습니다.

* multiplicity - 연산자 그룹의 mulitplicity.
* multiplicity_index - 이 연산자의 여러 인스턴스를 구별하는 데 사용할 수 있는 [0, multiplicity) 범위의 정수입니다.

Inports and Outports
----------

각각 `api.get_inport_names()` 및 `api.get_outport_names()` 메소드를 호출하여 
현재 operator 인스턴스에 대한 입력 및 출력 포트의 이름을 가져올 수 있습니다.

포트 이름을 key로 하고 연결 여부를 나타내는 boolean 값을 가지는 `api.is_inport_connected` 및 
`api.is_outport_connected` dictionary을 사용하여 어떤 inport 또는 outport가 연결되어 있는지 확인할 수 있습니다.

Example:
```python
if api.is_outport_connected["outport1"]:
    r = do_some_expensive_calculation()
    api.send("outport1", r)
```

Message type
------------

api 객체의 Message 유형은 `api.Message`로 접근할 수 있습니다.
다음과 같이 메시지 유형을 작성할 수 있습니다.
`api.Message(body, attributes)`, 여기서 body는 모든 객체가 될 수 있고 
attribute는 객체에 대한 str의 dictionary이거나 None이어야 합니다.
body 인수는 필수인 반면 attribute은 선택 사항이며 기본값은 None입니다. 
message 객체 'msg'의 body과 attribute은 각각 `msg.body`와 `msg.attributes`로 접근할 수 있습니다.

Correspondence between Modeler types and python types
-----------------------------------------------------

Modeler 유형은 operator 포트에서 허용되는 유형입니다.
예를 들어 `blob` 유형의 입력 포트가 있는 경우 
포트 콜백에 대한 인수로 수신할 Python 객체는 `bytes` 유형입니다. 
연산자의 출력 포트 유형이 `string`인 경우
출력 포트에 `str` 유형의 Python 객체를 보내야 합니다.

| Modeler | Python3     |
|---------|-------------|
| string  | str         |
| blob    | bytes       |
| int64   | int         |
| uint64  | int         |
| float64 | float       |
| byte    | int         |
| message | api.Message |

Python 연산자 포트 유형을 `python36`으로 설정할 수도 있습니다. 이 경우 
이 포트를 다른 Python 연산자에만 연결할 수 있습니다.
이것은 Python 특정 데이터 유형을 다른 Python 연산자에게 보내야 하는 경우에 유용할 수 있습니다. 
그룹 경계를 넘는 `python36` 포트 간의 연결은 허용되지 않으며 런타임 오류가 발생합니다.

FAQ
---
#### Operator의 초기화 코드는 어디에 배치해야 합니까?

스크립트는 한 번만 실행됩니다. 정의된 콜백 함수
스크립트에서 여러 번 실행할 수 있지만 스크립트의 가장 바깥쪽 범위의 명령은 한 번만 실행됩니다. 
이는 스크립트 본문에 초기화 코드를 간단히 배치할 수 있음을 의미합니다. 예를 들어:

```python
# Hypothetical script for Python3Operator

# In the operator's initialization, we might want to setup a connection
# with a database, for example (`setup_connection` is an hypothetical function):
db = setup_connection(api.config.host, api.config.port)

def my_callback_func(data):
    global db
    db.write(data)  # hypothetical call

api.set_port_callback("input", my_callback_func)
```

또는 `api.add_generator(func)`로 등록된 generator 콜백에 초기화 코드를 넣을 수도 있습니다.

