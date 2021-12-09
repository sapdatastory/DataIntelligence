`Table Producer` Operator
===========

This operator reads from any structured operators and produces a table in the specified database. 

Supported databases:

- SAP HANA (HANA_DB)
- SAP HANA Data Lake Database (HDL_DB)
- SAP IQ (SAP_IQ)

**Note**: This operator produces runtime metrics, which are described [here](./service/v1/parse/readme/general/docu/flowagent/metrics/README.md).

Configuration parameters
------------

* **Service**: The database where the tabular data is written

    ID: `service` | Type: `string` 

* **Connection ID**: Connection ID of the target system.

    ID: `serviceConnection` | Type: `object`

* **Target**: Remote dataset of the target object 

    ID: `source` | Type: `object`

Enter the required target table information based on the selected database type.

If SAP IQ or SAP HANA Data Lake database is selected, the following property is available:

* **Bulk load error toleration** (optional): Define the number of rows that can have an error for each failure including: unique, null, data value, and foreign key.

    ID: `sapiqBulkLoadErrors` | Type: `object`

    * **Unique errors** (optional): Number of unique errors to be tolerated.

        ID: `uniqueErrors`| Type: `number` | Default: `0`

    * **Null errors** (optional): Number of null errors to be tolerated.

        ID: `nullErrors` | Type: `number` | Default: `0`

    * **Data value errors** (optional): Number of data value errors to be tolerated.

        ID: `dataValueErrors` | Type: `number` | Default: `0`

    * **Foreign key errors** (optional): Number of foreign key errors to be tolerated.

        ID: `foreignKeyErrors` | Type: `number` | Default: `0`


* **Mode** (optional): Write mode.

	- Append: Add data to an existing table. When append is selected, the aditional option `Update records based on primary key` is shown. When this option is selected, the records already in the table are updated if the primary key is the same as a new record being appended. This behavior is the same as using an UPSERT SQL command. If `Update records based on primary key` is not selected and a collision on the primary key happens, then an error is thrown and the graph fails.

	- Overwrite: Drop the table and create another one according to the source schema.

	- Truncate: Clear the table before inserting data.

    ID: `mode` | Type: `string` | Default: `"overwrite"`


* **Maximum Batch Size**: The maximum number of records from the source included in each batch. The actual number of records is automatically calculated based on the dataset definition. To disable the automatic calculation, set the Use Defined Batch Size option to True. 

    ID: `batchSize` | Type: `integer` | Default: `1000`

* **Use Defined Batch Size**: Set to True when the automatic calculation does not provide optimal performance. When set to True, each batch of records contains the number of records entered in the Maximum Batch Size option. For example, when Maximum Batch Size is set to 1000, and Use Defined Batch Size is set to True, then there are 1000 records in each batch. When set to False, then each batch is between 10 and 1000 rows.

    ID: `forceBatchSize` | Type: `boolean` | Default: `false`

Bulk Loading
-----------------
Whenever possible, bulk load is enabled for improved loading performance.

* __SAP IQ__: Bulk load is enabled by default for all sources unless there is a BLOB datatype in the source. If there are BLOB objects, remove them using SQL consumer operators or by creating a view in the source. If it is not possible to remove the BLOB objects, this operator loads the data via the regular loading, which might be slow. The bulk load uses a `LOAD TABLE` statement, relying on named pipes to transfer the data file to the target. To use the `LOAD TABLE` statement, the SAP IQ user must have the following permissions in the server: `LOAD TABLE` and `ALLOW_READ_CLIENT_FILE`. The user might have to be the owner of the table, have database administrator authority, or have ALTER table permission to use the LOAD TABLE statement, depending on the '-gl' property used to start the SAP IQ server.

* __SAP HANA Data Lake Database__: Bulk load is enabled by default for all sources unless there is a BLOB datatype in the source. If there are BLOB objects, remove them using SQL consumer operators or by creating a view in the source. If it is not possible to remove the BLOB objects, this operator loads the data via the regular loading, which might be slow. The bulk load uses a `LOAD TABLE` statement, relying on named pipes to transfer the data file to the target. To use the `LOAD TABLE` statement, the HDL DB user must have the following permissions in the server: `LOAD TABLE` and `ALLOW_READ_CLIENT_FILE`. The user might have to be the owner of the table, have database administrator authority, or have ALTER table permission to use the LOAD TABLE statement.

Ports
------------
Input
------------

* **inTable**: Table type port, which comes as output from other structured operators.

    Type: `table`


Output
------------

* **out**: Outputs a scalar containing the name of the object that was written:

	Type: `scalar` | vType-ID: `com.sap.core.string`

	Output headers: 
	
	- `com.sap.headers.batch`
	- `com.sap.headers.producer`
	- `com.sap.headers.partition` (if consumer is configured with partition)
