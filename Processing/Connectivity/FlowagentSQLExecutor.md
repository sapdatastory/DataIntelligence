`Flowagent SQL Executor` Operator
===========

This operator performs a SQL Statement to any supported database. It uses Flowagent subengine to connect to the database. The specific SQL syntax depends on the specified database.

It provides a way to run SQL commands such as CREATE, INSERT, DELETE, and UPDATE in the database source.
Multiple commands can be provided, where they must be separated by a specified separator (default is `;`).
The output will be `success` if the commands were successfully run in the source. If a command fail, it will throw an error, which the `error` port will catch if it is mapped.

Supported Databases:

- Azure SQL DB (AZURE_SQL_DB)
- DB2 Database (DB2)
- Google BigQuery (GCP_BIGQUERY)
- SAP HANA Database (HANA_DB)
- SAP HANA Data Lake Database (HDL_DB)
- Microsoft SQL Server (MSSQL)
- MySQL Database (MYSQL)
- Oracle Database OSS (ORACLE)
- Redshift Database (REDSHIFT)
- SAP IQ Database (SAP_IQ)
- Snowflake Database (SNOWFLAKE)

Configuration parameters
------------

* **Connection ID**: Connection ID of the source system.

    ID: `serviceConnection` | Type: `object`

* **SQL Statement(s)** (optional): SQL statement(s) that are standard to the source. Statements must be separated by a specified separator.

    ID: `sqlStatements` | Type: `string` | Default: `""`

* **Separator** (optional): Separator that will be used to split the input into SQL statements.

    ID: `separator` | Type: `string` | Default: `";"`


* **Additional Session Parameters** (optional): Set session parameters that affect the connection with the source.

    ID: `additionalSessionParameters` | Type: `string` | Default: `""`


Ports
------------

Input
------------

* **sql**: SQL statement(s) that are standard to the source. Statements must be separated by a defined separator.

    Type: `scalar` | vType-ID: `com.sap.core.string`


Output
------------

* **result**: Output `success` if the commands where successfully executed.

    Type: `scalar` | vType-ID: `com.sap.core.string`


* **error**: If mapped, the operator errors are sent to this port and the graph continues running. If not mapped, the graph terminates with the operator error.

    Type: `structure` | vType-ID: `com.sap.error`
