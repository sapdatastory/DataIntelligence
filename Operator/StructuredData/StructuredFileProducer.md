`Structured File Producer` Operator
===========

This operator reads from any structured operators and produces a file (CSV, ORC, or PARQUET) in the specified storage. 

Supported cloud storages:

- Azure Data Lake (ADL)
- Azure Data Lake V2 (ADL_V2)
- Google Cloud Storage (GCS)
- HDFS
- Amazon S3 (S3)
- Alibaba OSS (OSS)
- Semantic Data Lake (SDL)
- Windows Azure Storage Blob (WASB)

**Note**: This operator produces runtime metrics that are described [here](./service/v1/parse/readme/general/docu/flowagent/metrics/README.md).

Configuration parameters
------------

* **Service**: The storage where the tabular data is written

    ID: `service` | Type: `string` 

* **Connection ID**: Connection ID of the target system.

    ID: `serviceConnection` | Type: `object`

* **Target**: Remote dataset of the target object 

    ID: `source` | Type: `object`

* **Mode** (optional): Defines the write mode for CSV files. Options are Overwrite and Append. Overwrite replaces the existing content, while Append adds data to an existing file. In both cases, if the file does not exist yet, it is created during the writing process. **Important**: GCS, S3, and WASB do not allow append.

    ID: `mode` | Type: `string` | Default: `"overwrite"`


* **Format** (optional): The supported cloud storage output file formats include CSV, PARQUET, and ORC. The CSV file conforms to the [RFC-4180 specification](https://tools.ietf.org/html/rfc4180), where the row delimiter is always CRLF and the escape character is always double-quotes.

    ID: `format` | Type: `string` | Default: `"CSV"`


* **CSV Properties**: Properties of the CSV output.

    ID: `additionalProperties_csv` | Type: `object`


    * **Column delimiter** (optional): The field separator. These characters are supported: , ; | : TAB.

        ID: `columnDelimiter` | Type: `string` | Default: `","`


    * **Header Included** (optional): Indicates whether each CSV output has a header as the first line.

        ID: `csvHeaderIncluded` | Type: `boolean` | Default: false


* **Additional Properties**: Additional properties related to the upload options to cloud storage. It is only applicable when a cloud storage service is selected.

    ID: `additionalProperties_common` | Type: `object`


    * **Compression type** (optional): Compression type used when uploading file into cloud service.

        ID: `compressionType` | Type: `string` | Default: `"None"`


* **Maximum Batch Size**: The maximum number of records from the source included in each batch. The actual number of records is automatically calculated based on the dataset definition. To disable the automatic calculation, set the Use Defined Batch Size option to True. 

    ID: `batchSize` | Type: `integer` | Default: `1000`

* **Use Defined Batch Size**: Set to True when the automatic calculation does not provide optimal performance. When set to True, each batch of records contains the number of records entered in the Maximum Batch Size option. For example, when Maximum Batch Size is set to 1000, and Use Defined Batch Size is set to True, then there are 1000 records in each batch. When set to False, then each batch is between 10 and 1000 rows.

    ID: `forceBatchSize` | Type: `boolean` | Default: `false`


* **Write part files** (optional): Defines whether the writer produces a single file or a directory of files.

    ID: `writePartFiles` | Type: `boolean` | Default: `false`


* **Limit part file records** (optional): Defines whether to limit individual partition files with a maximum number of records.

    ID: `limitPartFileRecords` | Type: `boolean` | Default: `false`


* **Max part file records** (optional): Indicates the maximum number of records in each partition file. This guarantees that partition files will not exceed this number.

    ID: `maxPartFileRecords` | Type: `integer` | Default: `100000`


* **Part file write mode** (optional): Defines the write mode for partition files. Options are Overwrite and Append. Overwrite deletes the existing directory if it was a partition file directory and re-create it. Append adds new files to an existing partition file directory. Important: If appending, the producer must match the existing format of the partition file directory, including the format and column layout.

    ID: `partFileWriteMode` | Type: `string` | Default: `"Append"`


Placeholders
------------

For file names, we support the following placeholders:

 * ```<sourceTableName>``` : When connected to a table consumer, this placeholder is replaced by the table name of the source. For SQL consumers, this placeholder is replaced by `SQL_Table`. Note: unsupported characters (anything besides alphanumeric characters, a hyphen, and a period) are replaced with an underscore.
 * ```<counter>``` : An incremental integer for each file written, starting with 1.
 * ```<date>``` : The date at the moment of writing, in the format `yyyyMMdd`. 
 * ```<time>``` : The time at the moment of the writing, in the format `HHmmss`.
 * ```<timestamp>``` : The timestamp at the moment of the writing, in the format `yyyyMMdd_HHmmss`. 
 * ```<partitionName>``` : The partition number if the consumer has partitions. For example, 0, 1, and so on. Important: If the consumer has partitions, and the number is not specified, the partition number is always appended to the file name to avoid concurrency issues during writing.

Remote file name conventions
------------

Each cloud provider has its own naming convention for defining bucket and object names. Follow these conventions to avoid any source-related issue.

Even though operators accept most special characters, we recommend that only alphanumeric characters are used. This avoids any undesired issues because all sources work well with such characters. Furthermore, some special characters such as `"`, `+`, and `,` are not allowed by the Flowagent File Producer operator and should not be used.

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

