`Read HANA Table` Operator
===============
com.sap.hana.readTable.v2

**Input**<br>
input (type: none)<br>
**Output**<br>
success (type: table)<br>
error (type: structure)<br>

Read HANA Table 연산자는 SAP HANA의 테이블에서 데이터를 읽을 수 있습니다.

Configuration parameters
------------

* **Connection** (mandatory): The object containing the connection parameters to a HANA instance.<br>
    ID: `connection` | Type: `object` | Default: `{}`

* **Configuration Mode**: Specifies how the operator determines the table (and which of its columns) to be read.<br>
    ID: `configMode` | Type: `string` | Default: `"Dynamic (from input)"`

    Accepted values:

    - _Static (from configuration)_: the operator does not expect any input. It reads from the table identified in `Table name`. If `Columns` is empty, all columns are retrieved. After outputting all relevant data, the operator becomes idle.
    - _Dynamic (from input)_: the operator uses each input message to determine the name of the source table and which columns to fetch. More details available in the **Input** section below.
* **Table Name**: The name of the source table in **Static** mode.<br>
    ID: `tableName` | Type: `string` | Default: `""`

* **Columns**: The list of columns that are retrieved in **Static** mode.
    ID: `columns` | Type: `array` | Default: `[]`

* **Decimal Output Format**: Determines how the operator outputs the values for columns of type `DECIMAL` and `SMALLDECIMAL` in string format.
    ID: `decimalOutputFormat` | Type: `string` | Default: `"Fraction"`

    Accepted values:

    - _Fraction_: decimals are represented as string in `"<numerator>/<denominator>"` format (For example, `"3/4"`).
    - _Floating-point_: decimals are converted to double-precision floating-point numbers represented as string. Note that the resulting number may not represent the exact value of the division as there can be a loss of precision.

* **CESU-8 Output Handling**: Determines how the operator deals with CESU-8 encoding problems. Such situation can happen due to the conversion from UTF-16 (used in ABAP systems) to CESU-8 or UTF-8 used internally to represent the values as strings. This affects only character-based field types.<br>
    ID: `cesu8Handling` | Type: `string` | Default: `"Default"`

Accepted values:
```shell
* *Default*: the operator throws an error describing the column and row that caused the problem.
```

Example:
```shell
invalid CESU-8: <FIELD_VALUE> at pos: <POSITION> row: 0 fieldname: <COLUMN_NAME>

* *Replace*: incorrectly encoded CESU-8 characters are replaced with the Unicode replacement character (`'\uFFFD'`).
* *Raw*: the data of all character-based columns is represented by the exact bytes stored in the database field with no transformation.
```

* **Read Mode**: Determines how the operator should read the table. Only used in **Static** mode.<br>
    ID: `readMode` | Type: `array` | Default: `[]`

    Accepted valued:

    - _Once_: the operator reads the table only once, then becomes idle.
    - _Poll_: the operator periodically polls the table for data.
* **Poll Period**: When **Read Mode** is set to **Poll**, this property determines the interval between consecutive queries.<br>
    ID: `pollPeriod` | Type: `string` | Default: `"1s"`

* **Batching**: Determines how the operator’s output should be batched.<br>
    ID: `batching` | Type: `string` | Default: `"None"`

    Accepted values:

    - _None_: no batching is performed. All rows in the target table are sent in a single output.
    - _Fixed size_: the output is broken into separate messages whose size is dictated by **Batch Size**. When placed in a group with multiplicity, the different instances of the operator take measures to avoid repetition. Refer to the **Multiplicity** section below for details and examples.
* **Batch Size**: When **Batching** is set to **Fixed size**, this property determines the number of rows in each output.<br>
    ID: `batchSize` | Type: `integer` | Default: `100`

* **Connection Timeout**: The maximum amount of time to wait for the server. If at any time the operator does not hear from the server within this period of time, the connection is closed. If set to zero, the operator waits for the server indefinitely.<br>
    ID: `connectionTimeout` | Type: `string` | Default: `"50s"`

* **Error Handling**: Details available here.<br>
    ID: `errorHandling` | Type: `string` | Default: `"terminate on error"`


Input
------------
* **input**: An input with an empty body containing the `com.sap.headers.hana.table` header with specific table details. This is only applicable in **Dynamic** mode. Kind: `none` Type ID: `""`

Output
------------
* **success**: A dynamic Table described in the header `com.sap.headers.hana.table` together with the queried rows. Kind: `table` Type ID: `*`

* **error**: An error message as described here. It depends on the **Error Handling** configuration. Kind: `structure` Type ID: `com.sap.error`

State Management Support
-----
State management support is provided when **Mode** is set to Static and **Batching** is set to Fixed size, with _at-least-once_ guarantee.

The state is saved between batches, so upon recovery, the operator doesn’t have to start reading the table from the start. Instead, the read starts from the last batch index saved once the graph is resumed.

Multiplicity
-----
When configured to perform fixed-size batching, this operator takes its multiplicity into account when performing queries. Its instances progressively query the table in chunks of **Batch Size** rows, avoiding overlaps. Since each instance performs a separate query for each chunk, keep in mind that simultaneous changes to the source table may affect the behavior of this operator.

As an example, consider a source table of 65 rows and a **Read HANA Table** operator with multiplicity 3 and **Batch Size** 10. Assuming the table remains unchanged during execution, the following reads might take place (note that, due to concurrency, the order of events is not reliable):

* instance 0 outputs rows 0–9, 30–39 and 60–65;
* instance 1 outputs rows 10–19 and 40–49;
* instance 2 outputs rows 20–29 and 50–59.
