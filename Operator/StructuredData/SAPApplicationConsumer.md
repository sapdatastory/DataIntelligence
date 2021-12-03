`SAP Application Consumer` Operator
===========

This operator reads from a variety of SAP and non-SAP applications. The operator produces structured output, and you need to connect it to other operators from the Structured Operators category. For example, [Data Transform](./service/v1/documentation/com.sap.datatransform.v2) or [Structured File Producer](./service/v1/documentation/com.sap.storage.producer.v3).

Custom Editor
-----------

This operator uses a custom editor user interface, which is described [here](./service/v1/parse/readme/general/docu/flowagent/custom_editor/README.md).

Configuration parameters
------------

* **Service**: The application from where to consume tabular data.

    ID: `service` | Type: `string` 

* **Connection ID**: Connection ID of the source system.

    ID: `serviceConnection` | Type: `object`

* **Source**: Remote dataset of the selected source object

    ID: `source` | Type: `object`

* **Trace level** (optional): Trace level of the extraction

    ID: `traceLevel` | Type: `string` | Default: `""`

* **Default (N)VARCHAR Size**: The default size of a varchar. The valid range is 0-5000.

    ID: `defaultColumnSize` | Type: `string` | Default: `"1024"`

* **Batch Query**: Determines whether the query is performed in batches. When true, the query to the OData source is performed batch by batch. Each batch is the size specified in **Fetch Size**.

    ID: `batchQueryMode` | Type: `boolean` | Default: `"false"`

* **Maximum Fetch Size**: The maximum number of records from the source included in each batch. The actual number of records is automatically calculated based on the dataset definition. To disable the automatic calculation, set the Use Defined Fetch Size option to True.

    ID: `fetchSize` | Type: `integer` | Default: `1000`

* **Use Defined Fetch Size**: Set to True when the automatic calculation does not provide optimal performance. When set to True, each batch of records contains the number of records entered in the Maximum Fetch Size option. For example, when Maximum Fetch Size is set to 1000, and Use Defined Fetch Size is set to True, then there are 1000 records in each batch. When set to False, then each batch is between 10 and 1000 rows.

    ID: `forceFetchSize` | Type: `boolean` | Default: `false`

* **Access Method**: Open Connectors API used for retrieving data. In *GET* mode, Open Connectors' data query API is called directly once per page to retrieve data. In *BULK* method, an asynchronous query job is created at Open Connectors and then starts streaming data.

    ID: `accessMethod` | Type: `string` | Default: `"GET"`
    
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


