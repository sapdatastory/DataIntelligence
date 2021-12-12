Python3 Operator 처리 예제
===

# 1. File to File 처리
None

# 2. DB to File 처리
## 2.1 Read HANA Table Operator : table <-> table Type
![](images/4.HanaPython.png)<br>
Read HANA Table --> Python3 --> Table to Binary --> Binary File Producer --> Graph Terminator

```python
import random

# Starts the random seed
random.seed()

# Function that adds a column to the end of each row of the input table
def add_column(table):
    for r in table:
        r = r.append(random.randint(-1000, 1000))
    return table

# Function called when input data is received
def forward_table(_, header, ibody):
    # Gets a reader to read the input table as a stream
    table_reader = ibody.get_reader()
    
    # Here we read the whole table at once as on this scenario the input comes in batches that should be of a relatively small size
    # The api however allows reading it partially and sending that to the output, only closing after all the data has been sent
    table = table_reader.read(-1)
    
    # Modify the table to showcase the api
    table = add_column(table)
    
    # Infer the type of the input table, necessary as we're working with dynamic types
    type_ref = table.infer_dynamic_type()
    
    # Set the output type to the dynamic type inferred
    api.outputs.outTable.set_dynamic_type(type_ref)
    
    # Define a writer to send the table as a stream to the output using the same input headers
    _, w = api.outputs.outTable.with_writer(header)
    
    # Write the table to the output
    w.write(table)
    
    # Close the output writer, indicating to the next operator that the stream is over
    w.close()

# Bind the input port to the function to handle it
api.set_port_callback("input", forward_table)
```

## 2.2 Run HANA SQL Operator : table <-> table Type
![](images/7.HanaPython.png)<br>
Run HANA SQL --> Table to Binary --> Binary File Producer --> Graph Terminator

```python
select * from DI_DEMO.PRODUCT
```

# 3. DB to DB 처리
## 3.1 Read HANA Table Operator : table <-> table
![](images/4.HanaPython.png)<br>
Read HANA Table --> Python3 --> Init HANA Table --> Write HANA Table --> Graph Terminator

```python

```

# 4. 기타
## 4.1 Static to Dynamic Converter : table(Static) <-> table(Dynmic) Type
![](images/3.HanaPython.png)<br>
Python(Static) --> Python(Dynamic) --> Terminal

```python
# Creates and outputs a static table
def create_table():
    # Example table
    table = api.Table([
            [1, "hello"],
            [2, "world"]
        ])
        
    # Create the writer to send the output as a stream
    _ , writer = api.outputs.outStatic.with_writer()
    
    # Here we write the table as a whole, but writes of a few rows at a time are allowed
    writer.write(table)
    
    # After writing the whole table we close the writer to indicate the end of the stream
    writer.close()
    
# Set the function to run during the start of the operator
api.set_prestart(create_table)
```
```python
prev_type_ref = None

# Receives a static table on the input and outputs a dynamic table
def on_input(_, iheader, ibody):
    global prev_type_ref
    
    # Defines the buffer size so we don't read the whole table at once, avoiding loading the whole table to memory at once
    bufferSize = 100
    
    # Gets a reader for the input table
    table_reader = ibody.get_reader()
    
    # Start reading the input table
    table = table_reader.read(bufferSize)
    
    # Use the table data to infer a compatible dynamic type
    if not prev_type_ref:
        prev_type_ref = table.infer_dynamic_type()
    type_ref = prev_type_ref
    
    # Use the dynamic type inferred to set the output type
    api.outputs.outDynamic.set_dynamic_type(type_ref)
    
    # Create a writer to send data to the output via stream
    _ , writer = api.outputs.outDynamic.with_writer()
    
    # Loop until no more data is available on the input
    while len(table) > 0:
        # Send the current buffer to the output
        writer.write(table)
        
        # Reads the next rows
        table = table_reader.read(bufferSize)
        
    # Close the output stream after reading all of the input data
    writer.close()

# Set the function to run when data is sent on the input port named "input"
api.set_port_callback("input", on_input)
```

## 4.2 Dynamic to Static Converter : table(Dynamic) <-> table(Static) Type
![](images/3.HanaPython.png)<br>
Python(Dynamic) --> Python(Static) --> Terminal

```python
# Creates and outputs a dynamic table
def create_table():
    # Example table
    table = api.Table([
            [1, "hello"],
            [2, "world"]
        ])
    
    # Use the table data to infer a compatible dynamic type
    type_ref = table.infer_dynamic_type()
    
    # Use the dynamic type inferred to set the output type
    api.outputs.output.set_dynamic_type(type_ref)
    
    # Create a writer to send data to the output via stream
    _ , writer = api.outputs.output.with_writer()
    
    # Here we write the table as a whole, but writes of a few rows at a time are allowed
    writer.write(table)
    
    # After writing the whole table we close the writer to indicate the end of the stream
    writer.close()
    
# Set the function to run during the start of the operator
api.set_prestart(create_table)
```
```python
# Receives a dynamic table on the input and outputs a static table
def on_input(_, iheader, ibody):
    # Defines the buffer size so we don't read the whole table at once, avoiding loading the whole table to memory at once
    bufferSize = 100
    
    # Gets a reader for the input table
    table_reader = ibody.get_reader()
    
    # Since we know the output type we don't need to infer it, so we can create the writer now
    msg_id, writer = api.outputs.outStatic.with_writer()

    # Start reading the input table
    table = table_reader.read(bufferSize)
    
    # Loop until no more data is available on the input
    while len(table) > 0:
        # Send the current buffer to the output
        writer.write(table)
        
        # Reads the next rows
        table = table_reader.read(bufferSize)
        
    # Close the output stream after reading all of the input data
    writer.close()

# Set the function to run when data is sent on the input port named "input"
api.set_port_callback("input", on_input)
```
