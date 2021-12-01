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
`api.send` 함수를 호출하여 데이터를 출력 포트로 보낼 수 있습니다.

아래 예에서는 문자열 `data` 객체를 출력 포트 `out`에 씁니다.
```python
# assuming that there is an output port named 'out'
data="some string"
api.send('out', data)
```

출력 데이터의 유형이 `out` 포트의 Modeler 유형과 호환되지 않는 경우 오류가 발생하여 그래프가 실패할 수 있습니다. 포트 유형을 선택하려면 `Correspondence between Modeler types and Python types` 섹션을 참조하세요.

Working with callbacks
------
콜백 사용을 예시하기 위해 수신된 데이터를 인쇄하는 간단한 함수를 정의하겠습니다.
```python
def on_data_in(datain):
    print(datain)
```

`api.try_port_callback` 함수를 사용하여 이 함수를 콜백으로 사용하는지 테스트할 수 있습니다. 지정된 포트의 데이터로 콜백을 한 번 실행합니다. 이 기능은 대화형 모드에서만 사용할 수 있습니다.

`api.try_port_callback` 실행 중 예외가 발생하면 노트북 커널에서 예외가 발생하고 그래프 상태는 영향을 받지 않습니다. 예외 및 스택 추적은 마지막 활성 셀 출력에 인쇄됩니다.
```python
# assuming that there is an input port named 'in'
api.try_port_callback('in', on_data_in)
```

참고: `on_data_in`이 `print` 기능을 호출하면 수신된 데이터가 Jupyter 노트북 UI의 마지막 활성 셀에 인쇄된 것을 볼 수 있습니다.

`on_data_in` 함수를 테스트하고 원하는 동작에 맞게 조정한 후 `api.set_port_callback`을 호출하여 입력 포트 `in`에 대한 콜백으로 함수를 등록할 수 있습니다.

이렇게 하면 입력 포트 `in`에 새 메시지가 있을 때마다 콜백 `on_data_in`이 호출됩니다.
```python
# assuming that there is an input port named 'in'
api.set_port_callback('in', on_data_in)
```

`api.set_port_callback` 함수로 등록된 콜백 실행 중 예외가 발생하면 파이썬 서브 엔진에 예외가 기록되고 그래프는 실패합니다.

Unregistering a callback
-------------------------
콜백을 등록 해제하여 더 이상 실행되지 않게 하려면 `api.remove_port_callback` 함수를 매개변수로 함수와 함께 사용할 수 있습니다.
```python
api.remove_port_callback(on_data_in)
```

Registering callbacks to multiple ports
-------------------------
여러 포트에 콜백을 등록하려면 등록하려는 포트 수와 동일한 수의 매개변수를 받는 함수가 필요합니다.
```python
 
def on_multiple_inputs(input1, input2):
    pass

# assuming that there are two input ports: 'in1', 'in2'
api.set_port_callback(['in1', 'in2'], on_multiple_inputs)
```

Running in Productive mode
-----
Jupyter 운영자는 'productive' 모드에서 실행할 수 있으므로 셀을 실행하는 데 사용자 상호 작용이 필요하지 않습니다. 이 모드는 Modeler UI의 운영자 설정에서 선택하여 구성 매개변수 'Productive'을 `False`에서 `True`으로 전환할 수 있습니다.

생산 모드에 있을 때 생산으로 태그가 지정된 셀은 사용자 상호 작용 없이 실행됩니다. Jupyter 노트북 UI에서 각 셀 상단에서 탭을 찾을 수 있습니다. 셀에 태그를 지정하려면 탭의 텍스트 상자에 원하는 태그(이 경우 `productive`)를 입력하고 'Add tag' 버튼을 클릭합니다.
```shell
def my_productive_code(value):
    send('out', value)
    
api.set_port_callback('in', my_productive_code)
```
참고: - 생산적인 코드가 `productive` 태그로 생산적인 것으로 표시되지 않은 셀의 다른 코드를 참조하는 경우 운영자가 이 모드에서 비생산적인 코드를 무시하고 그래프가 실패하기 때문에 런타임 오류가 발생합니다. 따라서 모든 관련 코드 셀을 `productive`으로 표시해야 합니다. - 생산 모드에서 실행할 때 Jupyter 노트북 UI에 액세스하여 셀과 상호 작용할 수 없습니다. - 런타임 시 실행 모드를 변경할 수 없습니다. 이를 변경하려면 그래프를 중지하고 '생산적' 구성을 원하는 값으로 설정한 다음 그래프를 다시 시작해야 합니다.

Accessing the configuration object
-----
`api.get_config`를 호출하여 Modeler에서 연산자 구성의 UI에 설정된 구성 개체를 가져올 수 있습니다. 예를 들어, 현재 노트북의 위치를 얻으려면 구성 개체에서 "notebookPath" 키에 액세스할 수 있습니다.
```python
config = api.get_config()
config["notebookPath"]
```

Installing python modules
-----
add_dependency 함수를 사용하여 Python 모듈을 설치할 수 있습니다.

아래 예에서는 `api.add_dependency`를 사용하여 `h5py` 모듈을 설치합니다.
```python
api.add_dependency("h5py")
```

Working with messages
----
`Message`를 호출하여 Message 유형에 액세스할 수 있습니다. 메시지 개체 `msg`의 본문 및 속성은 각각 `msg.body` 및 `msg.attributes`로 액세스할 수 있습니다.

Message(body, attributes)
-----
```python
Args:
    *body (object): body of the message
    attributes(dict(str, object) | None): attributes of the message
```
Example:
```python
msg = Message(None,{"debug": True, "config": {}})
```

Predefined Functions
-----
현재 Jupyter 노트북 내부에서 사용할 수 있는 6가지 기능이 있습니다.

- `api.send(port, data)`
- `api.get_config()`
- `api.add_dependency(package_name)`
- `api.try_port_callback(ports, callback)`
- `api.set_port_callback(ports, callback)`
- `api.remove_port_callback(callback)`

짧은 설명을 보려면 함수 이름(코드 셀 내부) 위에 있는 `Shift-Tab`을 누르고 전체 설명을 보려면 `Shift-Tab-Tab`을 눌러 Jupyter 노트북 UI 내에서 언제든지 함수 문서에 액세스할 수 있습니다.

#### api.send(port, data)
    Writes the data to the specified operator output port. Be careful with the correspondence between the Python data object and the Modeler port type.
    Args:
        port (str): operator's output port name
        data: data object to send
        
#### api.get_config()
    Returns the Jupyter operator's configuration object
    Args:
        None
    Returns:
        config(dict): configuration object

#### api.add_dependency(package_name)
    This method tries to install a Python package using pip. If the installation fails, an exception is raised.

    Args:
        package_name (str): Name of the package to be installed with pip.

#### api.try_port_callback(ports, callback)
    This method executes the callback once with the data retrieved from the specified input ports. The callback is called only when there are messages available in all input ports.
    * Note that this function is available only in interactive mode.
    Args:
        ports (str|list[str]): input ports to be tested with the callback. `ports` can be a list of strings with the name of each port to be associated, or a string if you want to associate the callback with a single port.
        callback (func[...]): a callback function with the same number of arguments as elements in `ports`. The arguments are passed to `callback` in the same order as their corresponding ports in the `ports` argument. 
    
#### api.set_port_callback(ports, callback)
    This method associates the input ports with the callback. The callback is called only when there are messages available in all input ports. If this method is called multiple times for the same group of ports, then the previous callback is overwritten by the provided one.
    Different ports group cannot overlap. For example, a port can be only associated with one callback at a time.
    Args:
        ports (str|list[str]): input ports to be associated with the callback. `ports` can be a list of strings with the name of each port to be associated, or a string if you want to associate the callback with a single port.
        callback (func[...]): a callback function with the same number of arguments as elements in `ports` or a variable-length argument. The arguments are passed to `callback` in the same order as their corresponding ports in the `ports` argument.

#### api.remove_port_callback(callback)
    Unregister the callback function. If the function is not registered, the method exits quietly.

    Args:
        callback (func[...]): callback function to be removed.
    
Correspondence between Modeler types and Python types
-----
Modeler 유형은 운영자 포트에서 허용되는 유형입니다. 예를 들어 `blob` 유형의 입력 포트가 있는 경우 포트 콜백에 대한 인수로 수신할 Python 객체는 `bytes` 유형입니다. 이제 연산자의 출력 포트에 `string` 유형이 있으면 출력 포트에 `str` 유형의 Python 객체를 보내야 합니다.
| Modeler | Python3     |
|---------|-------------|
| string  | str         |
| blob    | bytes       |
| int64   | int         |
| uint64  | int         |
| float64 | float       |
| byte    | int         |
| message | Message     |

