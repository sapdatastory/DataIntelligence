# `Table to Binary` Operator

Encodes table data in a serialization data format.

## Configuration parameters

- **Output Format** (mandatory)<br>
  The serialization format for the output data.<br>
  ID: `outputFormat` | Type: `string` | Default: `CSV` | Possible values: `CSV`, `JSON`, `JSONLINES`, `Parquet`

- **Collect Batches** (mandatory)<br>
  Indicates whether the input data shall be collected in batches. If set to `true`, input batches are collected until the last batch is received, and only then is the output provided.
  If the input does not contain a "com.sap.headers.batch" header and if set to `true`, then the input stream will be collected (if `streamSize` is not set to `-1`) and a single output is generated.<br>
  ID: `collectBatches` | Type: `boolean` | Default: `false` | Possible values: `true`, `false`

- **Column Separator** (mandatory if `outputFormat` is `CSV`)<br>
  The character that shall be used in the output CSV string to separate data columns. (Visible if `outputFormat` is `CSV`.)<br>
  ID: `colSep` | Type: `string` | Default: `,`

- **Row Separator** (mandatory if `outputFormat` is `CSV`)<br>
  The character that shall be used in the output CSV string to separate data rows. If set to `OS` the OS specific line terminator will be used. (Visible if `outputFormat` is `CSV`.)<br>
  ID: `rowSep` | Type: `string` | Default: `LF` | Possible values: `CR`, `LF`, or `CRLF`

- **Include Header Row** (mandatory if `outputFormat` is `CSV`)<br>
  Indicates whether a header row containing the column names shall be included in the output CSV string. (Visible if `outputFormat` is `CSV`.)<br>
  ID: `header` | Type: `boolean` | Default: `true` | Possible values: `true`, `false`

- **Column Names**<br>
  A string specifying the column names as a comma separated list. If `header` is set to `true` this will override the column names specified in the table metadata. (Visible if `outputFormat` is `CSV`.)<br>
  ID: `colNames` | Type: `string` | Default: none

- **Decimal Separator**<br>
  The character that shall be used in the output CSV string to separate the integer part from the fractional part of a number in decimal form. (Visible if `outputFormat` is `CSV`.)<br>
  ID: `decSep` | Type: `string` | Default: `.`

- **Escape Character**<br>
  A character that shall be used in the output CSV string to escape characters that would otherwise be interpreted as having a special function. (Visible if `outputFormat` is `CSV`.)<br>
  ID: `escapeChar` | Type: `string` | Default: none

- **Quoting Character**<br>
  The character that shall be used in the output CSV string to denote the start and end of a quoted item. (Visible if `outputFormat` is `CSV`.)<br>
  ID: `quoteChar` | Type: `string` | Default: ``

- **Datetime Format String**<br>
  A string containing a Python format specification for date or datetime values. (Visible if `outputFormat` is `CSV`.)<br>
  ID: `dateFormat` | Type: `string` | Default: none

- **Format** (mandatory if `outputFormat` is `JSON`)<br>
  The format in which the data is represented in the output JSON string. (Visible if `outputFormat` is `JSON`.)
  ID: `format` | Type: `string` | Default: `records` | Possible values: `split`, `records`, `index`, `columns`, `values`, `table`
  
| Format | Syntax |
|--------|--------|
| `split` | { "index": [ \<index value\>, ... ], "columns": [ \<column name\>, ... ], "data": \<data in `values` format\> } _where_ \<index value\> _is an index identifying each data row_ |
| `records` | [ { \<column name\>: \<value\>, ... }, ... ] |
| `index` | { \<index value\>: { \<column name\>: \<value\>, ... }, ... } |
| `columns` | { \<column name\>: { \<index value\>: \<value\>, ... }, ... } |
| `values` | [ [ \<value\>, ... ], ... ] |
| `table` | { "schema": \<schema\>, "data": \<data in `records` format\> } _where_ \<schema\> _is:_ { "fields": [ { "name": \<column name\>, "type": \<column type\> }, ... ], "primaryKey": [ \<pk column name\>, ... ] } _where_ \<column type\> _is one of_ "string", "number", "integer", "boolean", "datetime" |

A full specification of the schema that can be used with the `table` format can be found at https://specs.frictionlessdata.io/table-schema/.

- **Compression Type**<br>
  The type of compression that shall be used for the output data. If not specified no compression will be applied. (Visible if `outputFormat` is `Parquet`.)<br>
  ID: `compression` | Type: `string` | Default: none | Possible values: `snappy`, `gzip`, or `brotli`

- **Partitioning Columns**<br>
  A string containing a comma separated list of column names by which to partition the data. Columns are partitioned in the order they are given. If not specified no partitioning will be applied. (Visible if `outputFormat` is `Parquet`.)<br>
  ID: `partitionCols` | Type: `string` | Default: none

## Input

- **table** (type `table`, vtype-id `*`)

  Input data table.

## Output

- **binary** (type `scalar`, vtype-id `com.sap.core.binary`)

  The input table data serialized in the specified format. For the output formats `CSV` and `JSONLINES`, the operator is streaming new line delimited records to the output, while for the other output formats, a processing of the full table at once is required. The opened stream is sending bytes to the consumer, and therefore the consumer has to ensure a proper handling of the stream as incomplete records can be consumed (for example, streaming byte chunks to a file). If the consumer relies on complete records, then the consumer can make use of the new line delimiter while consuming the byte stream.

- **error** (type `scalar`, vtype-id `com.sap.error`)

  An error that occurred during the conversion.

<br>
