Python3 Operator
===============

Python3 연산자를 사용하면 `api` 객체가 제공하는 몇 가지 편의 기능을 제공하는 스크립트를 정의할 수 있습니다. 예를 들어 `api.set_port_callback("datain", callback_name)`을 작성하여 "datain" 포트에 수신된 모든 새 데이터에 대해 호출되는 콜백을 설정할 수 있습니다.
`api`가 제공하는 기타 편의 사항은 다음과 같습니다.

Python3 연산자의 확장은 **Repository** 탭을 선택하여 Modeler에서 직접 생성할 수 있습니다.

> 참고: 이 연산자는 python 3.6에서 실행됩니다.

> 참고: 스크립트에 등록된 각 콜백은 **different thread** 에서 실행됩니다.
> 스크립트 개발자는 경쟁 조건과 같은 잠재적인 동시성 문제를 처리해야 합니다. 
> 예를 들어 Python [threading module](https://docs.python.org/3/library/threading.html)의 
> 기본 요소를 사용하여 해당 문제로부터 보호할 수 있습니다.

**경고**: 다음 버전인 2113에서는 Python 3.6이 3.9로 업데이트됩니다. 연산자가 제공하는 API는 변경할 필요가 없습니다. 주요 호환되지 않는 변경 사항은 `async` 및 `await`를 예약어로 추가하고 asyncio 모듈과 함께 사용하는 것입니다. 새로운 기능의 전체 목록은 다음에서 찾을 수 있습니다.

- https://docs.python.org/3/whatsnew/3.7.html

- https://docs.python.org/3/whatsnew/3.8.html

- https://docs.python.org/3/whatsnew/3.9.html

그러나 연산자가 사용하는 패키지에는 주요 변경 사항이 포함될 수 있습니다. 버전의 패키지 변경은 tornado `5.0.2`에서 `6.1.0`으로, pandas `1.0.3`에서 `1.2.5`로 입니다. Tornado 목록은 https://github.com/tornadoweb/tornado/blob/stable/docs/releases/v6.0.0.rst에서 확인할 수 있습니다. 이는 연산자에게 영향을 미치지 않을 것으로 예상됩니다. Pandas에는 주요 변경 사항이 없습니다. 그러나 사용되지 않는 기능은 경고를 생성합니다. 목록은 https://pandas.pydata.org/pandas-docs/dev/whatsnew/v1.2.0.html에서 찾을 수 있습니다. 3.6에서 사용된 패키지 중 일부는 3.9에서 작동하기 위해 새 버전이 필요할 수 있습니다.

Configuration parameters
------------

* **script** (mandatory): Inline script to be executed. If **script** starts with "file://", it specifies the path to the script file.  
  ID: `script` | Type: `string` | Default: `""`

Input
------------
* **None**

Output
------------
* **None**

Basic Examples
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
    Send `data` to outport named `port`.

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
    Multiple distinct periodic callbacks can be added. If an already added callback is added again, the old period
    is replaced by the new `period`. Timers are not preemptive. Thus, the given interval provides only the
    lower bound of the interval at which the timer function is called.
    A zero `period` implies that the callback is called as fast as possible.
    If you want two callbacks with identical behaviour to be run
    simultaneously then you need to create two different functions with identical body or
    create a factory function that defines an inner function and returns it. Each time the factory function
    is called, a new function (with different id) is returned - but with identical behaviour. See the tip
    in the set_port_callback section to see an example of a factory function.

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
This example produces value 0,1,2... on port "output" until graph shutdown.

#### api.remove_timer(callback)
    Deregister timer callback.

    Args:
        callback (func): Callback function to be removed.

#### api.update_timer(period, callback)
    Update the period of an existing `callback`.
    No error is thrown if the callback does not exist.

    Args:
        callback (func): Callback function for which the period is updated. If `callback` is not registered,
                         nothing changes.
        period (str): String number representing a new period to overwrite the old value.

Shutdown handlers
------
Shutdown handlers are functions that are executed in the order they are added after the operator stop event.
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
The `api` object provides the possibility to read configurations defined on the operator´s editor view or added in the configuration panel in the graph´s view. If you define a config named "foo", you
can access it by calling `api.config.foo`. Configuration field names cannot contain spaces. The "script" and "codelanguage" config fields do not appear in `api.config` as
they are mandatory configuration parameters and should not be used.
If you add a json object to a configuration field in the Modeler, it becomes a dictionary in Python.

Logging
-------
To log messages, use `api.logger.info("some text")`, `api.logger.debug("")`, `api.logger.warn("")`, or `api.logger.error("")`.

Error handling
-----
You can raise any exception inside the script. As a result, the exception message is logged and the operator is
terminated - except if the exception is thrown inside a thread different than the script's main thread. In this case,
you need to call `api.propagate_exception(e)`, where **e** is the exception object to handle it correctly.

> Note: Do not write to stderr because that could have unintended consequences. Also, do not use `api.logger.fatal` or `api.logger.critical`, otherwise the graph stops. Raise an exception or use `api.propagate_exception` if you want to stop the graph and log the error.

Halting execution
-----------------

If you want to halt the graph's execution with an error, follow the instructions from the **Error handling** section.
To stop the graph without an error, a **Python Operator** can send a signal to a **Graph Terminator Operator**.

If it is necessary to only stop the operator's execution (without stopping the graph as a whole), you can deregister all its callbacks.
Notice that stopping a single operator can lead the data flow in the graph as a whole to stop.

Note: Be aware that using the Python command `sys.exit(code)` causes only the current Python thread to exit and we do not recommend its use.
We also do not advise using the Python command `os._exit(code)`, which causes the whole Python process to abort and the graph to stop with an error.
If you want the whole graph to stop with an error, follow the instructions from the **Error handling** section.

repo_root and subengine_root
----------------------------

You can access the repo_root and subengine_root path using api.repo_root and api.subengine_root, respectively.

graph_name, graph_handle and group_id
-------------------------------------

You can access the graph_name, graph_handle and group_id values using api.graph_name, api.graph_handle and api.group_id, respectively.

* graph_name - identifier of a saved graph. Example: com.sap.dataGenerator
* graph_handle - unique identifier of the graph instance. It is referred as Runtime Handle in the modeler user interface 
* group_id - unique identifier of the group where the operator is running 

multiplicity, multiplicity_index
--------------------------------

Two variables can be accessed to obtain multiplicity-related information api.multiplicity and api.multiplicity_index:

* multiplicity - the multiplicity of the operator's group.
* multiplicity_index - an integer in the range [0, multiplicity) that can be used to distinguish the multiple instances of this operator.

Inports and Outports
----------

You can get the name of the input and output ports for the current operator instance by
calling the methods `api.get_inport_names()` and `api.get_outport_names()`, respectively.

You can check which inports or outports are connected by using the `api.is_inport_connected` and `api.is_outport_connected`
dictionaries which have the name of the port as key and a boolean indicating whether it is connected as value.

Example:
```python
if api.is_outport_connected["outport1"]:
    r = do_some_expensive_calculation()
    api.send("outport1", r)
```

Message type
------------

You can access the Message type in the api object as `api.Message`.
The message type can be built such as the following:
`api.Message(body, attributes)`, where body can be any object and
attributes should be a dictionary of str to object, or None.
The body argument is mandatory while attributes is optional and
defaults to None. The body and attributes of a message object `msg` can be
accessed as `msg.body` and `msg.attributes`, respectively.

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
#### Where should I place initialization code for my operator?

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

