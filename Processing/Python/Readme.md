Python3 Operator
===============

With the Python3 operator you can define a script that offers some convenience functions provided by the `api` object. As an example, you can set up a callback that is called for every new data received in the "datain" port by writing `api.set_port_callback("datain", callback_name)`.
Other conveniences provided by `api` are described below.

An extension of the Python3 Operator can be created directly in the Modeler by choosing the **Repository** tab.

> Note: This operator runs on python 3.6.

> Note: each callback registered in the script runs in a **different thread**.
> As the script developer, you should handle potential concurrency issues such as race
> conditions. You can, for instance, use primitives from the
> Python [threading module](https://docs.python.org/3/library/threading.html)
> to get protected against said issues.

**Warning**: In the next version, 2113, Python 3.6 will be updated to 3.9. APIs provided by the operator do not require changes. The main incompatible change is the addition of `async` and `await` as reserved words and their use with the asyncio module. The complete list of new features can be found at:

- https://docs.python.org/3/whatsnew/3.7.html

- https://docs.python.org/3/whatsnew/3.8.html

- https://docs.python.org/3/whatsnew/3.9.html

However, packages used by the operator can include breaking changes. The package change of versions are: tornado `5.0.2` to `6.1.0` and pandas `1.0.3` to `1.2.5`. The Tornado list of news can be found at https://github.com/tornadoweb/tornado/blob/stable/docs/releases/v6.0.0.rst. These are not expected to affect operators. Pandas has no breaking changes. Deprecated features generate a warning, though. The list can be found at https://pandas.pydata.org/pandas-docs/dev/whatsnew/v1.2.0.html. Keep in mind some of the used packages with 3.6 can require new versions to work with 3.9.

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
Count all incoming messages on the "input" port and write the count to the "output" port.
```python
counter = 0

def on_input(data):
    global counter
    counter += 1
    api.send("output", counter)

api.set_port_callback("input", on_input)
```

Notice that "output" port of an operator containing the above script should be of type `int64`, since the variable `counter` is of Python type `int`. See `Correspondence between Modeler types and python types` for more information on how to choose your port types.

`api.set_port_callback` can also be used to wait for two input ports to have received data before calling the handler:

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
    This method associates input `ports` to the `callback`. The `callback` is only called when there are
    messages available in all `ports`. If this method is called multiple times for the same port group,
    the old `callback` is replaced by a new one. Different port groups cannot overlap. The same callback
    function cannot be reused in different port groups.

    Args:
        ports (str|list[str]): input ports to be associated with the callback. `ports` can be a list of strings
                               with the name of each port to be associated or a string if you want to associate the
                               callback to a single port.
        callback (func[...]): a callback function with the same number of arguments as elements in `ports` or a variable length argument.
                              The arguments are passed to `callback` in the same order of their corresponding
                              ports in the`ports` list.

TIP: If you want to reuse the same callback function in multiple
port groups, you can have a function that returns your function of interest:
```
def get_my_callback():
  def my_callback(data):
      # some code here
  return my_callback

api.set_port_callback("inport1", get_my_callback())
api.set_port_callback("inport2", get_my_callback())
```
This way, a new function (with different id) is generated
each time, but the callback behaviour remains the same.

#### api.remove_port_callback(callback)
    Deregister the `callback` function. If it does not exist, the method exits quietly.

    Args:
        callback: Callback function to be removed.

Generators
------
Generators are functions that are executed before the event processing loop starts. They are executed in the order they are added.
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
This example produces values 0,1,2,3,4,5 on the output port "output".

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

The Modeler types are the ones that are allowed in the operator ports.
For example, if you have an input port of type `blob` then the Python object
that you are going to receive as argument to your port callback is
of type `bytes`. If the output port of your operator has type `string`,
you should send a Python object of type `str` in its output
port.

| Modeler | Python3     |
|---------|-------------|
| string  | str         |
| blob    | bytes       |
| int64   | int         |
| uint64  | int         |
| float64 | float       |
| byte    | int         |
| message | api.Message |

You can also set a Python operator port type to `python36`. In this case,
you are able only to connect this port to other Python operators.
This can be useful if you need to send Python
specific data types to other Python operators. Note that connections between
`python36` ports that cross group boundaries are not allowed, and leads
to runtime error.

FAQ
---
#### Where should I place initialization code for my operator?

The script is executed just once. The callback functions defined
in the script can be executed multiple times, but the commands from the
script's outermost scope are executed just once. This implies that
you can simply place initialization code in the body of the script. For example:

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

Alternatively, you can also place initialization code in a generator
callback that is registered with `api.add_generator(func)`.

<br>
<div class="footer">
   &copy; 2020 SAP SE or an SAP affiliate company. All rights reserved.
</div>
