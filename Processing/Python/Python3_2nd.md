Python 3
========

Python3 연산자를 사용할 때 `api` 객체가 제공하는 몇 가지 편의 기능을 제공하는 스크립트를 정의할 수 있습니다. 예를 들어 `api.set_port_callback("datain", callback_name)`을 작성하여 "datain" 포트에 새 데이터를 수신할 때 호출되는 콜백을 설정할 수 있습니다.

Python 3 연산자를 확장하는 연산자는 Modeler의 **Repository** 탭에서 직접 생성할 수 있습니다.

> 이 연산자는 Python 3.6에서 실행됩니다.

Configuration Parameters
------------

* **script** (mandatory): Inline script to be executed. If script starts with "file://", then the script file is executed.  
  ID: `script` | Type: `string` | Default: `""`
  
* **Error handling** (mandatory): Defines how the operator treats exceptions during `prestart`, `port callbacks`, and `timer callbacks`. During `shutdown`, an exception will terminate the graph if this has not been triggered before. More details at the `Error Handling` section. 
  ID: `errorHandling` | Type: `string` | Default: `"terminate on error"`
  
  Accepted values:

  * *terminate on error*: exceptions terminate the graph.
  * *log and ignore*: exceptions are logged and the operator continues running.
  * *propagate to error port*: exceptions are sent to the error port and the operator continues running. It assumes a port called `error` of type `structure` and `com.sap.error` has been created.
    It is possible to create a custom exception named `OperatorException` to provide more details like: `code`, `text`, `details`.
  * *retry*: exceptions are communicated through response callback. More details at the `Error Handling` section. 

Input
------------
* **None**

Output
------------
* **None**

Basic Examples
------
이 snipphet은 이름이 "input"이고 유형(scalar, "com.sap.core.int64")인 포트에서 들어오는 모든 message를 계산하고 "output"이라는 포트와 유형(scalar, "com.sap.core.txt")에 개수를 씁니다. int64").

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
    Publish `data` and `header` to outport named `port`.

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
    Publish the first `n` bytes from `data` (assumed to be a file object) and `header` to outport named `port`. If `n` is -1, a parallel stream connection is created and data is transfered through it.

> Output is possible only after operator initialization. Therefore, only during prestart, timer, and port callbacks.

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
    Create a stream writer to outport named `port`.
    In the case of a dynamic port, api.outputs.port.set_dynamic_type should be previously called. For more details, see section "Working with Dynamic Types".

> Output is possible only after operator initialization. Therefore, only during prestart, timer, and port callbacks.

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
    Publish `none` type, which only contains headers and no body data, to outport named `port`.

> Output is possible only after operator initialization. Therefore, only during prestart, timer, and port callbacks.

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

For an example, see section "Working with dynamic types".
    
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
This example produces values 0,1,2 on the output port "output".

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
This example produces value 0,1,2... on port "output" every 0,1,2... seconds until graph shutdown.


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
The `api` object provides the possibility to read configurations defined on the operator´s editor view or added in the configurations panel in the graph´s view. If you defined a config named "foo" you
can access it by calling `api.config.foo`. Configuration field names cannot contain spaces. The "script" and "codelanguage" config fields don't appear in `api.config` as
they are mandatory configuration parameters and should not be used.
If you filled a config field with a JSON object in the Modeler, its value becomes a dictionary (in Python).

> This operator does not support additional configuration included by the Configuration tab in the Modeler UI. However, configurations can still be included directly in the graph JSON, similar to `errorHandling` and `codelanguage`.

Logging
-------
To log messages, use `api.logger.info("some text")`, `api.logger.debug("")`, `api.logger.warn("")`, or `api.logger.error("")`.

App Logging
-----------
> Each call to these functions results in an HTTP request. This can affect performance.
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

Given the four `error handling` options, only `propagate to error port` needs further support in the operator script.
This option triggers messages to the `error` port following the [Error Message format](./service/v1/parse/readme/general/docu/errors/README.md).
The operator allows customization of `code`, `text`, and `details` by raising `api.OperatorException`.
If this exception type is not used, the `com.sap.error` message will have default values: `code` as `0`, `text` as `exception message`, and empty `details`.

#### api.OperatorException(code, text, details)
    An exception to customize the `com.sap.error` message when `propagate to error port` is being used. 
  
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

In general, it is possible to raise any exception inside the script and have it treated according to the `error handling` configuration. 

If you want the exception to stop the operator, use `api.propagate_exception(e)` in the script, where e is the exception. 
Note: In case the exception is thrown inside a thread different than the script's main thread (the main thread is the one running the callbacks), the previous mentioned error handling configuration does not work. As a result, the script must rely on using `api.propagate_exception(e)` or sending the exception to the main thread.

Halting Execution
-----------------

If you want to halt the graph's execution with an error, follow the instructions from the **Error handling** section.
To stop the graph without an error, a **Python Operator** can send a signal to a **Graph Terminator Operator**.


Be aware that using the Python command `sys.exit(code)` causes only the current Python thread to exit, and we do not recommend its use.
We also do not advise using the Python command `os._exit(code)`, which causes the whole Python process to abort and the whole graph to stop with an error.
If you want the whole graph to stop with an error, follow the instructions in the **Error handling** section.

repo_root and subengine_root
----------------------------

You can access the repo_root and subengine_root path using api.repo_root and api.subengine_root, respectively.
Accessing any file or folder under the path `/vrep` is not supported and, while it is still possible to use such path, it is unadvised.

graph_name, graph_handle and group_id
-------------------------------------

You can access the graph_name, graph_handle and group_id values using api.graph_name, api.graph_handle and api.group_id, respectively.

* graph_name - identifier of a saved graph. Example: com.sap.dataGenerator
* graph_handle - unique identifier of the graph instance. It is referred as Runtime Handle in the Modeler. 
* group_id - unique identifier of the group where the operator is running.

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
dictionaries, which have the name of the port as key and a boolean indicating whether it is connected as value.

Example:
```python
if api.is_outport_connected["outport1"]:
    r = do_some_expensive_calculation()
    api.outputs.output1.publish({}, r)
```

Data Types
------

In the typing system of the Pipeline Engine, a data type is specified by its type and its ID. Its ID can belong to one of three categories:

- `scalar`
- `structure`
- `table`

The scalars are the most basic types of Modeler's typing system. Structures are a named and ordered collection of fields. Each field is of type scalar. This collection of data is called a Record. Tables are a collection of many Records, or more precisely, an ordered list of Records.

Scalar types are based on templates. The templates are a fixed set of type definitions.

New Data Types can be created through the Modeler in the Data Types section. Currently, only custom structures and tables can be defined.

You can find in the below table the relation between the core scalars, the type templates, and the Python type.


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


> :arrows_counterclockwise: Currently under development. Not available yet.

Note that, in the Modeler, the templates `decimal`, `date`, `time`, and `timestamp` are represented as a `string`. As a convenience for you when retrieving one of the following types, the object returned is converted to a high-level class for easier manipulation.

It is also possible to retrieve the raw string representation of the object by calling `.get_raw()`.

Data Type Reference
-----

To refer to data types, the API exposes the class `api.DataTypeReference`. It can be used to hold the type and ID in a single object.
#### api.DataTypeReference(type, ID)
    Args:
        type (str): "scalar", "structure" or "table"
        ID (str): ID from type

```python
int64_type = api.DataTypeReference("scalar", "com.sap.core.int64")
```


Type Context
-----

The type context provides access to methods that interact with the type system, such as checking if a type exists or creating a new dynamic type.
It can be accessed as an attribute of the API: `api.type_context`.

#### api.create_new_table(columns, keys)
    Creates a new dynamic table containing the specified columns. For an example, please check the section "Working with Dynamic Types".

    Args:
        columns (dic[str|api.DataTypeReference]): Dictionary mapping column names to their types.
        keys (List[str]): List containing the name of the key columns.

    Returns:
        ref (api.DataTypeReference): Reference to created type.

Working with Dynamic Types 
-----

Ports can be either static or dinamically typed. Static ports have a fixed type and ID, while dynamic ports keep the fixed type but allow for any type ID to be sent or received. One example is a dynamic table output that always outputs tables, but each table can have a different schema. The ID of a dynamic port is `*`.

When using dynamic ports to output data via streams using the `with_writer` interface, first, you must call `publisher.set_dynamic_type` to associate a type to the dynamic port.
When using the `publish` interface, if the data do not contain the type information, the engine tries to infer it.

In the following example, we create a new table type in runtime and associate it to our publisher before getting the writer:
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

In the next example instead of manually defining the columns, we would like to leave the engine infer it:
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
A Record is an iterable class that represents a collection of either scalars or tables. Its constructor can be called from `api.Record`. 

Its elements can be accessed via indexing.

> :arrows_counterclockwise: Currently under development. Not available yet.

It offers the following methods:

#### record.get_field_names()
    Returns (List(str)): list with the names of the fields that compose the structure.

#### record.get_field_type_ids()
    Returns (List(str)): list with the type IDs of the fields that compose the structure.

For the following example, let's assume an operator that has an input port `input1` of a fictional table of ID `my.simpleStructure`. This table contains 3 columns:

| Field Name                      | Field type     | Field id          | 
| --------------------------      | ------------   |  ------------      |
| id	                          | scalar         | com.sap.core.int64|
| name	                          | scalar         | com.sap.core.string|
| salary	                      | scalar         | com.sap.core.float64|


In the example code, we read the data from the input port and access the fields first using indexing and then by the name fields.

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
A Table is an iterable class that represents an ordered collection of rows. Its constructor can be called from `api.Table`.
Its elements can be accessed via indexing.

Tables can have a type associated to it or not. To have a typed table you can either pass the desired type on its constructor or call `infer_dynamic_type` to create a new dynamic type to represent it.

#### api.Table(data: List, type_id: str)
    Arguments:
      data (List): data to compose the table body. Excepts a List of rows, in other words, a list of lists.
      type_id (str, optional): ID from type to associate to it.

    Returns:
      new_table (api.Table): created api.Table

It offers the following methods:

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


> :arrows_counterclockwise: Currently under development. Not available yet.

#### table.to_pandas()
    Returns (pandas.DataFrame): Dataframe converted from the body of the table object.

Header
------
Read-only dictionary whose first level is expected to have `str` as keys and `List` or `api.Record` as values.

As the header is a read-only structure, to modify, you should call its `.copy()` method to get a `dict` representation of the received header. This prevents unexpected changes as operators could point to the same header.

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
The InputBody is the class that wraps up the incoming data. It is received in the callback along with the message ID and the headers. It gives access directly to the object received or to a stream, depending on the type of the port associated.

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
Object to write into Table streams. Note that particularly with tables it is possible to output the table as a batch. For example, use the publish function of the publisher as well.

It offers the functions:

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
Object to read from Table streams. There is no EOF signaling if writer closed the stream. Instead, an empty table. 

#### reader.read(n=-1)
    Read a list of rows from the stream and returns it in the table format. This function is blocked from returning if less than the desired number of rows is available and the stream is still open. If the stream is closed, read can return less than `n` rows. If `-1` is passed, rows are read until writer closes the stream.
    Args:
        n (int): Number of rows to be read.
    Returns:
        table (api.Table): Table object containing the read rows.

> :arrows_counterclockwise: Currently under development. Not available yet.
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
Object to write into Binary streams. Note that it is also possible to output the bytes as a batch. For example, using the publish function as well.

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
Object to read from a stream of bytes. If 0 bytes are returned, and the size was not 0, this indicates the end of the stream.

#### reader.read(n=-1)
    Read bytes from the stream. This function is blocked from returning if less than the desired number of bytes is available and the stream is still open. If the stream is closed, read can return less than n bytes. If -1 is passed, bytes are read until writer closes the stream.
    Args:
        n (int): Number of bytes to be read.
    Returns:
        data (bytes): bytes read.

Correspondence Type Templates, Python Types and dtypes
-----------------------------------------------------

When reading a table as a dataframe, if necessary, the individuals piece of the data from the table will be converted to a different format.

In the table below, you can find the expected dtype for an element of a scalar type after the conversion from the table format to a pandas dataframe.

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

In the presence of nulls, the corresponding value in a dataframe is of type pd.NA (not available). When nulls are present, then the columns have mixed types and the column dtype is object.

State Management
----------------

> This requires the graph to run with snapshot enabled. This directly affects the graph runtime but provides recovery.

This should be used if the operator is expected to run with state management enabled, and it has an internal state. This operator is referred to as stateful. By default, all not stateful operators do not need to implement the functions below.
To declare the operator stateful, it has to have the option set when calling `set_initial_snapshot_info`. In case it has a state, the operator has to implement at least `set_restore_callback` and `set_serialize_callback`.

Operators with support to state management can have two extra classes, generators and writers. Generators are further explained at `api.OutportInfo`. Writers are operators which have effects outside the graph. For example, operators writing into databases or writing to a publisher or subscriber queue.
If an operator is a writer, it will offer at-least-once guarantee if it is stateful. This means, there is a guarantee that no data is lost, even though it could be written twice. Keep in mind being stateful requires implementing the restore and serialize functions.
It is also possible to have exactly-once guarantee, this requires the writer to be idempotent on top of being stateful. Idempotency means equivalency when writing the same data several times.

The following are some general observations regarding state management and how operators can support it.
 - A port callback should not be blocked while waiting for another. This leads to a deadlock.
 - Before saving a state, the shutdown function is not paused. So, the shutdown function should not change the operator state.

The following example scripts show the state management functions usage. More details are described after it.

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

In general, it is not recommended to operators with support to state management to spawn new threads or processes that can change the internal operator state or send data to the output ports. If this cannot be avoided, the `set_pause_callback` and `set_resume_callback` have to be used.
An example would be if an operator starts a thread inside an input port callback, and this thread writes into output ports. This requires implementing the two functions and they could rely on `threading.Lock`. The pause callback can acquire the lock, while the resume callback would release it.

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

Alternatively, you can also place initialization code in the prestart function by registering a function with `api.set_prestart(func)`.

Note that output is possible only after operator initialization. Therefore, only during prestart, timer, and port callbacks.

