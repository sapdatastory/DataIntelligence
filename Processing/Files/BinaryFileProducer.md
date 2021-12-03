`Binary File Producer` Operator
====================

The Binary File Producer operator writes files to various services.

A write operation happens at every input, either targeting a single file or a partitioned file depending on the configured **File Mode**.

Each operation uses a connection according to the configured **Connection**. And uses a path according to the configured **Path Mode**.


Supported services are:  

- **Alibaba Cloud Object Storage Service (OSS)**. 
- **Amazon Simple Storage Service (S3)**. Note: also supports S3-compatible services.
- **Google Cloud Storage (GCS)**.
- **Hadoop Distributed File System (HDFS)**.
- **HANA Data Lake (HDL_FILES)**.
- **Microsoft Azure Data Lake (ADL)**.
- **Microsoft Azure Data Lake Gen. 2 (ADL_V2)**.
- **Microsoft Windows Azure Storage Blobs (WASB)**.
- **Semantic Data Lake (SDL)**. 
- **SSH File Transfer Protocol (SFTP)**.
- **Local File System**. Note: it does not use a Connection ID. It is the local file system of the environment in which the group containing this operator is running. Operators in a different group don't have access to it. Accessing any file or folder under the path `/vrep` is not supported and, while the operator may still run with such a configured path, it is unadvised.

Configuration Parameters
------------
    
* **Connection**: Points to the connection to write to. The connection configuration is detailed [here](./service/v1/parse/readme/general/docu/connection_gen2/dynamic/README.md). It uses the _[file connection attribute](./service/v1/parse/readme/general/docu/file/README.md)_.
    ID: `connection` | Type: `object` | Default: `{"configurationType":"From input"}` 

* **Path Mode** (mandatory): Indicates where the path is taken from.  
    ID: `pathMode` | Type: `string` | Default: `"Dynamic (from input)"`  
    Accepted values:
    * *Dynamic (from input)*: the path is taken from the input attributes (`file.path`).
    * *Static (from configuration)*: uses the **Path** configuration parameter.
    * *Static with placeholders*: uses the **Path** configuration parameter, allowing placeholders. More details at the **Path Placeholders** section are found further below in this document.

* **Path**: The path where the file is written to, relative to the connection being used. It must be in the [qualified name format](./service/v1/parse/readme/general/docu//qualifiedname/README.md). If the **Connection** is set with a connection ID, you may use the UI file browsing to set the path. Only available if **Path Mode** is set to *Static (from configuration)* or *Static with placeholders*.  
    ID: `path` | Type: `string` | Default: `/`

* **Mode**: Affects the behavior of the operation if the file already exists. If it does not exist, the operator always creates it.  
    ID: `mode` | Type: `string` | Default: `Create only`  
    Accepted values:
    * *Overwrite*: overwrites the existing file with the content.
    * *Append*: append the content to the end of the existing file.
    * *Create only*: doesn't change the file if it already exists. An error may or not be reported based on the **If file exists** configuration.

* **File Mode**: Indicates whether the target file is a single file or a partitioned file. More details on the behavior of both options on the **File Modes** section available further below in this document.
    ID: `fileMode` | Type: `string` | Default: `Single file`  
    Accepted values:
    * *Single file*: writes input to a simple, single file.
    * *Partitioned file*: writes input to a partitioned file, using batch information to determine which file to write to.

* **Error Handling**: Details available [here](./service/v1/parse/readme/general/docu/errors/v2/README.md).   
  ID: `errorHandling` | Type: `string` | Default: `"terminate on error"`

Input
------------

* **file**: A binary input whose body is used as the content to be written. The `connection` and `path` values from the `com.sap.headers.file` header may be used as well, according to the operator configuration.
    Kind: `scalar`
    Type ID: `com.sap.core.binary`

Output
------------

* **file**: An output with an empty body and the `com.sap.headers.file` header set with the metadata of the file written, particularly the fields `connection` and `path`. The output is sent only when the file is completely written, be it after the input for writing a single file or on the last input when writing a partitioned file.
    Kind: `none`
    Type ID: `""`

* **error**: An error message as described [here](./service/v1/parse/readme/general/docu/errors/v2/README.md).
    Kind: `structure`
    Type ID: `com.sap.error`


Path Placeholders
------------

Path placeholders allow dynamic values as part of the path. They can be invoked using angle brackets: the string `<counter>` is replaced by the result of the placeholder named `counter`. 

Some placeholders also have a suffix, defined after the colon separator (`:`). Example:  
The string `<header:headerName>` points to the placeholder `header` with the suffix `headerName`.
        
Available placeholders are:

* `counter`: An incremental integer.  
    Take the following path:  
    * `/folder/file_<counter>.txt`  
    
    It generates sequential operations on the paths:  
    * `/folder/file_000001.txt`
    * `/folder/file_000002.txt`
    * `/folder/file_000003.txt`
* `date`: The current local date in the format `YYYYMMDD`.
    Take the following path:  
    * `/folder/file_<counter>.txt` 
    
    It considers the server's current date (such as 01/16/2020 - January 16th 2020) and daily writing operations to generate the following paths:  
    * `/folder/file_20201216.txt`
    * `/folder/file_20201217.txt`
    * `/folder/file_20201218.txt`
    
    If more than one operation is performed on the same day, the date remains the same:
    * `/folder/file_20201216.txt`
    * `/folder/file_20201216.txt`
    * `/folder/file_20201216.txt`
* `time`: The current local time in the format `HHMMSS`.
    Take the following path:  
    * `/folder/file_<time>.txt`
   
    It considers the server's current time (such as 22h 27min 33s) and a writing operation performed at each second to generate the following paths:  
    * `/folder/file_102733.txt`
    * `/folder/file_102734.txt`
    * `/folder/file_102735.txt`
    
    If more than one operation occurs at the same second, the time remains the same:  
    * `/folder/file_102733.txt`
    * `/folder/file_102733.txt`
* `dirname`: The directory prefix extracted from the incoming path. Requires an input path attribute (`file.path`).
    Take the following path:  
    * `<dirname>/file.txt`
    
    Consider that the input port message has the `file` key attribute with the value object `{ "path": "/myfolder/mysubfolder/myfile.txt" }`, it generates:  
    * `/myfolder/mysubfolder/file.txt`
* `basename`: The base file name extracted from the incoming path. Requires an input path attribute (`file.path`).
    Take the following path:  
    * `/folder/<basename>`
    
    Consider that the input port message has the `file` key attribute with the value object `{ "path": "/mydir/mysubdir/myfile.txt" }`, it generates:  
    * `/folder/myfile.txt`
* `extension`: The extension extracted from the incoming path without the leading dot (`.`). Requires an input path attribute (`file.path`).
    Take the following path:  
    * `/folder/file.<extension>`
    
    Consider that the input port message has the `file` key attribute with the value object `{ "path": "/mydir/mysubdir/myfile.txt" }`, it generates:  
    * `/folder/fil.txt`
* `multiplicity`: The multiplicity of the operator's group.
    Take the following path:  
    * `/folder/file_<multiplicity>.txt`
    
    It uses the multiplicity total according to where the operator is located. Default is 1 when the operator is not grouped.
    If the operator is grouped and Multiplicity is set to 3, it generates:  
    * `/folder/file_3.txt`
* `multiplicityIndex`: An integer in the range [0,`multiplicity`) that can be used to distinguish the multiple instances of this operator.
    Take the following path:  
    * `/folder/file_<multiplicityIndex>.txt`
    
    If the operator is grouped and Multiplicity is set to 3, three instances of the Binary File Producer operator are generated, each with a different index (0, 1, and 2).
    It can generate one of the following paths, depending on which Binary File Producer performed the operation:  
    * `/folder/file_0.txt`
    * `/folder/file_1.txt`
    * `/folder/file_2.txt`
* `header`: Queries the input message for a specified header. Requires a suffix with the message attribute key to be queried. For example: `<header:my_header>`
    Take the following path:  
    * `/folder/file.<header:fileFormat>`
    
    Considering that the input port message has a `fileFormat` key header with the `csv` value, it generates:
    * `/folder/file.csv`
    
    If key header is `fileFormat` and its value `txt`, it generates:
    * `/folder/file.txt`


File Modes
------------

The behavior for the **Single file** mode is to write to the target path at each input, outputting the target file metadata on success.

Each input writes to the configured path. If **Path Mode** is _From input_, the path is always taken from the current input. If **Path Mode** is _Static with placeholders_, **Path Placeholders** are reevaluated at each input.

If on **Partitioned file** mode, a folder is created on the configured path, following the same rules from the **Single file** mode. Part files are written inside this folder, including an eventual indicator file at the end of the operation.

In this mode, the input messages must have the **batch header** information set, with the required **batch index** and **is last** fields. The index is used to write to different part files on the file system.

Each batch implies a different part file being written. All parts imply a single complete file write operation. Therefore, all the checks and path processing necessary for the operation happen once at the beginning of the complete file write operation. The beginning here is defined as the arrival of a message with the **batch index equal to 0**.

An example of a partitioned file on the file system is the following:

```
output.csv/
    _SUCCESS
    part-0000-1.csv
    part-0000-2.csv
    part-0000-3.csv
    part-abcd-1.csv
    part-abcd-2.csv
```

The part files follow this format:

```
part-<uuid>-<index>.<extension>
```

Where:

* **uuid** is a unique ID generated for each operation. Two parts can have the same **index** but different **uuid**, as shown in the example.
* **index** is given by the batch index sent via the batch header on the input message.
* **extension** is the same as the target file.

When the operation starts, the `_SUCCESS` indicator file is removed from within the folder to indicate an ongoing operation. Once the operation finishes, it is written again to indicate the last operation finished. The indicator file has no contents.

Each operator **Mode** has a different behavior when the **File Mode** is set to **Partitioned file**, as follows:

* **Overwrite** recursively removes a file or a directory and its contents on the target path, then starts writing the first batch.
* **Append** checks for the presence of a valid partitioned file on the path. A partitioned append can't be executed on a single file. If the check is successful, the indicator `_SUCCESS` file is removed, and the operation starts. Notably, the appended data starts on the **index** 0, with a different **uuid**.
* **Create Only** checks the destination path for the presence of a file or folder. If it is present, the operation fails; otherwise, it starts.

State Management Support
------------

When writing with **File Mode** set to **Single file**, no state management support is possible, as we don't support partial writes to the target file.

State management support is provided when **File Mode** is set to **Partitioned file**, with **Exactly once** guarantee. The state is saved between part file writes, so upon recovery, the graph doesn't have to start writing from the first file. Instead, writing starts from the first received index once the graph is resumed.

If the **Connection** is set to **Local File System**, no state management support is possible since a local file system no longer exists once the graph reaches the Completed, Dead, or Paused status.  

<br>
<div class="footer">
   &copy; 2021 SAP SE or an SAP affiliate company. All rights reserved.
</div>
