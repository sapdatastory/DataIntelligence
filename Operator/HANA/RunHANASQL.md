`Run HANA SQL` Operator
===============
com.sap.hana.runSQL.v2

**Input**<br>
input (type: scalar)<br>
**Output**<br>
success (type: table)<br>
error (type: structure)<br>

Run HANA SQL 연산자는 SAP HANA 데이터베이스에서 사용자가 제공한 SQL 문을 실행합니다.

Configuration parameters
------------

* **Connection** (mandatory): The object containing the connection parameters to a HANA instance.<br>
    ID: `connection` | Type: `object` | Default: `{}`

* **Mode**: Determines how the operator obtains the SQL code.
    ID: `mode` | Type: `string` | Default: `"Dynamic (from input)"`

    Accepted values:

    - _Static (from configuration)_: the operator executes the statement(s) specified in **SQL** and becomes idle.
    - _Dynamic (from input)_: the operator executes SQL statement(s) from each input message.
* **SQL**: The SQL statement(s) to be executed when in **Static** mode. This value is ignored in Dynamic mode.
    ID: `sql` | Type: `string` | Default: `""`
  
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

* **Transaction Level**: Determines how the operator should group statements into database transactions.
    ID: `transactionLevel` | Type: `string` | Default: `"Per input"`

    Accepted values:

    - _Per input_: a separate transaction is used for each input, and each transaction encompasses all statements in that input.
      In **Static** mode, this means that the entire code in **SQL** is executed in a single transaction.

    - _Per statement_: a separate transaction is used for each statement, regardless of whether they came from the same input message.

* **Batching**: Determines how the operator’s output should be batched.<br>
    ID: `batching` | Type: `string` | Default: `"None"`

    Accepted values:

    - _None_: batching is not used.
    - _Fixed size_: output is sent in batches of fixed size (specified in **Batch size**).
* **Batch Size**: The number of rows to output in each batch. This parameter is used only when **Batching** is set to _Fixed size_, and it must be an integer greater than zero.<br>
    ID: `batchSize` | Type: `integer` | Default: `100`

* **Connection Timeout**: The maximum amount of time to wait for the server. If at any time the operator does not hear from the server within this period of time, the connection is closed. If set to zero, the operator waits for the server indefinitely.<br>
    ID: `connectionTimeout` | Type: `string` | Default: `"50s"`

* **Error Handling**: Details available here.<br>
    ID: `errorHandling` | Type: `string` | Default: `"terminate on error"`


Input
------------
* **input**: A string containing SQL commands. This applies only to **Dynamic** mode.

    Kind: `scalar` | Type ID: `com.sap.core.string`

Output
------------
* **success**: A dynamic Table described in the header `com.sap.headers.hana.table` together with the retrieved data. For statements that do not query data, a table of type `com.sap.hana.affected` is sent containing the details of how many rows were `affected`. When statements execute DDL modifications, affected is sent as -1.

    Kind: `table` | Type ID: `*`

* **error**: An error message, if applicable (see **Error Handling**), as described here.

    Kind: `structure` | Type ID: `com.sap.error`

State Management Support
-----
State management support is provided when following configuration is used: - **Mode** set to `Static`; - **Transaction level** set to `Per statement`; - **Batching** set to `Fixed size`.

The state is saved between statements, when there is more than one, and between batches, when there is data output. The operator offers at-least-once guarantee by saving the last statement executed and the batch index, when applicable. Upon recovery, the execution starts after the last statement saved and the data output starts from the last batch offset.

