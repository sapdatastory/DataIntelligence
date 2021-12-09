`Table Consumer` Operator
===========

This operator reads from an specified Database table or view. The operator produces a structured output, and you need to connect it to other operators from Structured Operators category (for example [Data Transform](./service/v1/documentation/com.sap.datatransform.v2) or [Structured File Producer](./service/v1/documentation/com.sap.storage.producer.v3)).

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

**Note**: This operator produces runtime metrics, which are described [here](./service/v1/parse/readme/general/docu/flowagent/metrics/README.md).

**Note**: This operator supports Snapshot when reading data using partitions. To learn more about how to run resilient pipelines using partitions, click [here](./service/v1/parse/readme/general/docu/flowagent/resiliency/README.md).

Configuration parameters
------------

* **Service**: The Database from where to consume tabular data.

    ID: `service` | Type: `string`

* **Connection ID**: Connection ID of the source system.

    ID: `serviceConnection` | Type: `object`

* **Source**: Remote dataset of the selected source object

    ID: `source` | Type: `object`

* **Partition Type** (optional): Partitioning is used to enable data reading in parallel. In this case, the **consumer** and **producer** must be inside a group with multiplicity equal to the number of partitions.

    **Note**: Partition is not supported when this consumer operator is combined with the `Data Transform` operator.

    **Note**: `Row ID` and `Physical (Source Based)` are only available for the connection type ORACLE.

    ID: `partitionType` | Type: `string` | Default: `"None"`

* **Logical Partition Specification** (optional): For more information about partitioning, check the [documentation](./service/v1/parse/readme/general/docu/flowagent/logical_partition/README.md).

    ID: `partitionSpecification` | Type: `object`

* **Number of partitions** (optional): Specifies the number of partitions to divide the table data. When the partition type option is set to `Row ID`, then this option is mandatory.

    ID: `numberOfPartitions` | Type: `integer`

* **Additional session parameters** (optional): Set session parameters that affect the connection with the source.

    ID: `additionalSessionParameters` | Type: `string` | Default: `""`

* **Maximum Fetch Size**: The maximum number of records from the source included in each batch. The actual number of records is automatically calculated based on the dataset definition. To disable the automatic calculation, set the Use Defined Fetch Size option to True.

    ID: `fetchSize` | Type: `integer` | Default: `1000`

* **Use Defined Fetch Size**: Set to True when the automatic calculation does not provide optimal performance. When set to True, each batch of records contains the number of records entered in the Maximum Fetch Size option. For example, when Maximum Fetch Size is set to 1000, and Use Defined Fetch Size is set to True, then there are 1000 records in each batch. When set to False, then each batch is between 10 and 1000 rows.

    ID: `forceFetchSize` | Type: `boolean` | Default: `false`

Custom Editor
-----------

This operator uses a custom editor user interface, which is described [here](./service/v1/parse/readme/general/docu/flowagent/custom_editor/README.md).

Ports
------------
Input
------------

* **inTrigger**: Trigger to indicate that the operator should start processing. Note: The input port is optional. If the input port does not have a connection, then the operator starts when the graph starts running.

    Type: `scalar` | vType-ID: `com.sap.core.string`

Output
------------

* **outTable**: Table type port, which can be used to connect to other structured operators.

    Type: `table`

	Output headers:

	- `com.sap.headers.batch`
	- `com.sap.headers.partition` (if it is configured with partition)
