`Structured File Consumer` Operator
===========

This operator reads from any supported cloud storage. The operator produces structured output, and you need to connect it to other operators from Structured Operators category (for example [Data Transform](./service/v1/documentation/com.sap.datatransform.v2) or [Structured File Producer](./service/v1/documentation/com.sap.storage.producer.v3)).

Supported cloud storages:

- Azure Data Lake (ADL)
- Azure Data Lake V2 (ADL_V2)
- Google Cloud Storage (GCS)
- HDFS
- Alibaba OSS (OSS)
- Amazon S3 (S3)
- Semantic Data Lake (SDL)
- Windows Azure Storage Blob (WASB)

Configuration parameters
------------

* **Storage type** (mandatory): The storage from which the file is read. Additional parameters may depend on the selected cloud storage.

    ID: `service` | Type: `string` | Default: `""`

* **Source Connection**: Connection ID of the source system.

    ID: `serviceConnection` | Type: `object`

* **Source Object**: Remote dataset of the selected file

    ID: `source` | Type: `object`

* **Partition Type** (optional): Partitioning is used to enable data reading in parallel. In this case, the **consumer** and **producer** must be inside a group with multiplicity equal to the number of partitions.

    **Note**: Partition is not supported when this consumer operator is combined with the `Data Transform` operator.

    ID: `partitionType` | Type: `string`

* **Fail on string truncation** (optional): Indicates whether the reader should exit and fail if a string truncation has happened. This behavior happens when the length of a string in the metadata is smaller than the actual data in the source file. 

    ID: `failOnStringTruncation` | Type: `boolean` | Default: true
    
* **Maximum Fetch Size**: The maximum number of records from the source included in each batch. The actual number of records is automatically calculated based on the dataset definition. To disable the automatic calculation, set the Use Defined Fetch Size option to True.

    ID: `fetchSize` | Type: `integer` | Default: `1000`

* **Use Defined Fetch Size**: Set to True when the automatic calculation does not provide optimal performance. When set to True, each batch of records contains the number of records entered in the Maximum Fetch Size option. For example, when Maximum Fetch Size is set to 1000, and Use Defined Fetch Size is set to True, then there are 1000 records in each batch. When set to False, then each batch is between 10 and 1000 rows.

    ID: `forceFetchSize` | Type: `boolean` | Default: `false`


Remote source description limitation
------------

When you select a file to be read via the browsing UI, the UI will obtain the metadata definition for the file. There are three major limitations with this approach:

 1. CSV files do not have a metadata definition, so the application infers the metadata by looking at the file.
 The column properties like delimiter, escape character, text delimiter and charset can be modified in case the inference is wrong.
 1. Parquet and ORC files have a metadata definition, but they do not specify the length of strings, which default to 5000.
 1. JSON/JSONL files column definitions default to string(5000) for arrays and structures when not flattened.
 The flattening level property is used to control the level of flattening and can be modified to any level below the maximum value for modeling. Modifying the flattening level updates the metadata definition and the data preview.

Given these facts, the metadata can be wrong, and the job may fail. For strings, the default is to fail the job on strings truncation. However, the operator can be configured to tolerate string truncations by setting the **Fail on string truncation** property to **false**.

Custom Editor
-----------

This operator uses a custom editor user interface, which is described [here](./service/v1/parse/readme/general/docu/flowagent/custom_editor/README.md).

Ports
------------
Input
------------

* **inTrigger**: Trigger to indicate that the operator should start its execution. Note: The input port is optional. If the input port does not have a connection, then the operator starts when the graph starts running.

    Type: `scalar` | vType-ID: `com.sap.core.string`

Output
------------

* **outTable**: Table type port, which can be used to connect to other structured operators.

    Type: `table`

	Output headers: 
	
	- `com.sap.headers.batch`

