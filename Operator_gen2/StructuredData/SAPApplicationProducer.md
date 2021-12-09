`SAP Application Producer` Operator
===========

This operator reads from any structured operators, and produces a table in the specified target like oData and BW.

Notes:

------------

* BW Datastore Target 
	
    - BW only supports Advanced DataStore objects as target under /DATASTORE folder.

    - For BW DataStore object as target, the field Write Interface-Enabled should be checked in the BW system (under DataStore Object-> Modeling Properties -> Special Properties -> [] Write Interface-Enabled)

    - To preview BW DataStore data within the operator, an ABAP connection needs to be created in the 'Connection Management' application that is associated with the specified BW Connection. That ABAP connection then needs to be specified for the 'ABAP Connection ID' field for the BW Connection.

Configuration parameters
------------

* **Service**: The application where the tabular data is written

    ID: `service` | Type: `string` 

* **Connection ID**: Connection ID of the target system.

    ID: `serviceConnection` | Type: `object`

* **Target**: Remote dataset of the target object 

    ID: `source` | Type: `object`

* **Maximum Batch Size**: The maximum number of records from the source included in each batch. The actual number of records is automatically calculated based on the dataset definition. To disable the automatic calculation, set the Use Defined Batch Size option to True. 

    ID: `batchSize` | Type: `integer` | Default: `1000`

* **Use Defined Batch Size**: Set to True when the automatic calculation does not provide optimal performance. When set to True, each batch of records contains the number of records entered in the Maximum Batch Size option. For example, when Maximum Batch Size is set to 1000, and Use Defined Batch Size is set to True, then there are 1000 records in each batch. When set to False, then each batch is between 10 and 1000 rows.

    ID: `forceBatchSize` | Type: `boolean` | Default: `false`

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

BW Advanced Datastore Activation
------------

When the SAP Application Producer finishes writing to the Advanced DataStore object, the data needs to be activated on the BW system before it can be used. This can be done on the BW system by creating a [BW Process Chain](./service/v1/documentation/com.sap.dh.bwprocesschain). Configure the BW process chain to activate the data in the DataStore object referenced in the SAP Application Producer. After the Process Chain is configured, saved, and activated, use the BW Process Chain operator in a graph to invoke the process chain and activate the data via a pipeline graph.

To load the data to BW and then activate it via a Process Chain, create a graph that includes a pipeline operator that executes a graph that writes the data to the BW DataStore. Then chain that graph to a pipeline operator that executes the graph to call the Process Chain that activates the data.

