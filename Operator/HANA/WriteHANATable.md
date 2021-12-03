`Write HANA Table` Operator
===============
com.sap.hana.writeTable.v2

**Input**<br>
input (type: table)<br>
**Output**<br>
success (type: table)<br>
error (type: structure)<br>

이 연산자는 SAP HANA 데이터베이스의 하나 이상의 테이블에 데이터를 수집할 수 있습니다.

대상 테이블은 초기화 시(**Static** 모드에서) 또는 입력이 수신될 때마다(**Dynamic** 모드에서) 이미 존재해야 합니다. 테이블 생성이 동일한 파이프라인의 일부로 의도된 경우 **Initialize HANA Table** 연산자를 이 연산자와 함께 사용하는 것이 좋습니다.

Configuration parameters
------------
* **Connection** (mandatory): The object containing the connection parameters to a HANA instance.<br>
    ID: `connection` | Type: `object` | Default: `{}`

* **Configuration mode**: Determines how the operator obtains the target table name.<br>
    ID: `configMode` | Type: `string` | Default: `"Dynamic (from input)"`

    Accepted values:

    - _Static (from configuration)_: the operator ingests all incoming data into the table specified in **Table name**.
    - _Dynamic (from input)_: the operator uses each input message to determine the destination.

* **Table name**: The name of the table to be used as a fixed destination in **Static** mode.<br>
    ID: `tableName` | Type: `string` | Default: `""`

* **Statement type**: Determines whether data is to be ingested using an `INSERT` or an `UPSERT` statement.<br>
    ID: `statementType` | Type: `string` | Default: `"INSERT"`

* **Connection timeout**: The maximum amount of time to wait for the server. If the operator does not hear from the server within this period of time, the connection is closed. If set to zero, the operator waits for the server indefinitely.<br>
    ID: `connectionTimeout` | Type: `string` | Default: `"50s"`

* **Error Handling**: Details available here.<br>
    ID: `errorHandling` | Type: `string` | Default: `"terminate on error"`

Input
------------
* **input**: It depends on the Configuration Mode:

    - _Dynamic (from input)_: A dynamic table containing the `com.sap.headers.hana.table` header with complete DDL details, or at least the table name, as well as the data to be inserted.
    - _Static (from configuration)_: A dynamic table with the data to be inserted. The `com.sap.headers.hana.table` header with complete DDL details is not necessary in this case but is taken into account if provided (except for the table name).
    
    Kind: `table` | Type ID: `*`

Output
------------
* **success**: A table of type `com.sap.hana.affected` containing the details of how many rows were received and affected. The output also includes the header com.sap.headers.hana.table with details of the table and columns that were modified by the input and data received. Due to a limitation on the HANA driver side, it is not possible to keep track of the affected rows when there are LOB columns involved, so the output will contain a -1 for it instead.

    Kind: `table` | Type ID: `com.sap.hana.affected`

* **error**: An error message, if applicable (see **Error Handling**), as described here.

    Kind: `structure` | Type ID: `com.sap.error`

