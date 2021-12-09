`Initialize HANA Table` Operator
===============
com.sap.hana.initTable.v2

**Input**<br>
input (type: table)<br>
**Output**<br>
success (type: table)<br>
error (type: structure)<br>

이 연산자는 SAP HANA 데이터베이스에서 하나 이상의 테이블을 초기화할 수 있습니다.

Configuration parameters
------------

* **Connection** (mandatory): The object containing the connection parameters to a HANA instance.<br>
    ID: `connection` | Type: `object` | Default: `{}`

* **Configuration Mode**: Determines how the operator obtains the values for the table name, column specification, and primary key.<br>
    ID: `configMode` | Type: `string` | Default: `"Dynamic (from input)"`

    Accepted values:

    - Static (from configuration): the operator does not expect any input. It initializes a table based on the configuration properties **Table Name**, **Table Columns**, and **Primary Key**. It initializes the table as soon as it starts running, writes the relevant output, and becomes idle.
    - Dynamic (from input): the operator uses each input message to determine the name, columns, and primary key of the target table. These are obtained from the header `com.sap.headers.hana.table` as explained in the Input section below.

* **Initialization Mode**: Determines how the operator should initialize the table(s).<br>
    ID: `initMode` | Type: `string` | Default: `"Create"`

    If the table does not yet exist, the operator only creates it.

    If the table already exists:

    - _Create_: it performs no action.
    - _Truncate_: it empties the table using a `TRUNCATE` statement.
    - _Delete_: it empties the table using a `DELETE` statement.
    - _Drop (Restrict)_: it drops and re-creates the table using a `DROP (...) RESTRICT` statement.
    - _Drop (Cascade)_: it drops and re-creates the table using a `DROP (...) CASCADE` statement.
* **Table Name**: The name of the table that is initialized in **Static** mode.<br>
    ID: `tableName` | Type: `string` | Default: `""`

* **Table Columns**: The list of columns that are used in **Static** mode, if the table needs to be created. This is used only when the table does not yet exist or **Initialization** Mode is set to either Drop option.<br>
    ID: `tableColumns` | Type: `array` | Default: `[]`

* **Primary Key**: A list of column names to be used as a primary key in Static mode.<br>
    ID: `primaryKey` | Type: `array` | Default: `[]`

* **Table Type**: The type of table that is created.<br>
    ID: `tableType` | Type: `string` | Default: `"Row"`

    Accepted values:

    - _Row_
    - _Column_
* **Output Initialized Table**: Controls whether the table to be created when in Static mode should be sent via the output port.<br>
    ID: `outputInitializedTable` | Type: `bool` | Default: `false`

* **Connection Timeout**: The maximum amount of time to wait for the server. If at any time the operator does not hear from the server within this period of time, the connection is closed. If set to zero, the operator waits for the server indefinitely.<br>
    ID: `connectionTimeout` | Type: `string` | Default: `"50s"`

* **Error Handling**: Details available here.<br>
    ID: `errorHandling` | Type: `string` | Default: `"terminate on error"`

Input
------------
* **input**: A dynamic Table containing the `com.sap.headers.hana.table` header with complete DDL details that specifies the table to be initialized. This is only applicable in **Dynamic** mode. In **Static** mode, the inputs are simply forwarded to the next operator when the table defined in the configurations has been initialized.

Output
------------
* **success**: A dynamic Table with the header `com.sap.headers.hana.table` describing the table that was successfully initialized, with an empty body. In Static mode, the first output will be the initialized table, if **Output Initialized Table** is set to `true`. Any additional output will be a copy of the inputs received as explained above.

