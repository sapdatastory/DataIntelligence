`Data Transform` Operator
=======

The Data Transform operator in the SAP Data Intelligence Modeler provides wide variety of options available to meet your data transformation needs. This operator allows user to perform data transformations, such as projection, filter, column operations and join. It supports to be connected with other operators from Structured Operators category as sources and targets. 


**Drag and drop the connection form the structured consumer to this operator.**

**Create one or more data target inside the operator to be connected to producers operators.**

**Double-click on this operator in order to specify the transformation nodes.**


Configuration parameters
------------

* **definition**: The definition of a transformation pipeline.

    ID: `definition` | Type: `object`

    * **outputs**: The schema is derived from the out schema of the previously connected transform.

        ID: `outputs` | Type: `array`

    * **inputs**: The input schemas of the transformation pipelines. The schema is derived from the source dataset.

        ID: `inputs` | Type: `array`

    * **nodes**: The transformation operations.

        ID: `nodes` | Type: `array`

    * **tablemappings**: Schema mappings among inputs and outputs.

        ID: `tableMappings` | Type: `array`
        
**Note: Any unconnected output port results in a graph failure.**

Case Transform
------------
Specifies multiple paths in a single node. The rows are separated and each group is processed in different ways.
The Case transform simplifies branch logic in data flows by consolidating case or decision making logic in one transform. 
Paths are defined in an expression table.

**Data inputs**: Only one data flow source is allowed.

**Case condition expressions**: Create two or more case condition expressions. Choose one as the default expression to contain the remaining records when all other case expressions evaluate to false.

Union
------------
Combines incoming datasets, producing a single output dataset with the same schema as the input datasets.

**Data inputs**: Two data flow sources are allowed.

**Options**: Choose Union All when you want to merge all of the records. To remove any duplicate records, do not select this option.


Join design considerations and objective
------------

For more information how to design JOIN with resource and performance options like RANK and CACHE, check the [documentation]
(./service/v1/parse/readme/general/docu/flowagent/data_transform/join/README.md).

Additional Info
------------

* This operator does not work if it is connected to another Flowagent Data Transform operator or any operator that is not from the Structured Operators category.

