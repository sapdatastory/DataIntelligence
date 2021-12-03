# `Binary to Table` Operator

Decodes serialized data and provides the data in table format.

## Configuration Parameters

- **Input Format** (mandatory)<br>
  The serialization format of the input data.<br>
  ID: `inputFormat` | Type: `string` | Default: `CSV` | Possible values: `CSV`, `JSON`, `JSONLINES` `Parquet`, `ORC`

- **Output Batches** (mandatory)<br>
  Indicates whether the output data shall be provided in batches.<br>
  ID: `outputBatches` | Type: `boolean` | Default: `false` | Possible values: `true`, `false`

- **Batch Size (Rows)**<br>
  The size of output batches (specified as a number of rows) if `outputBatches` is set to `true`.<br>
  ID: `batchSize` | Type: `integer` | Default: none

- **Column Separator** (mandatory if `inputFormat` is `CSV`)<br>
  The character that is used in an input CSV string to separate data columns. If set to `unknown` the operator will try to detect the used column separator. (Visible if `inputFormat` is `CSV`.)<br>
  ID: `colSep` | Type: `string` | Default: `,`

- **Row Separator** (mandatory if `inputFormat` is `CSV`)<br>
  The character that is used in an input CSV string to separate data rows. If set to `OS` the OS specific line terminator will be used. (Visible if `inputFormat` is `CSV`.)<br>
  ID: `rowSep` | Type: `string` | Default: `LF` | Possible values: `CR`, `LF`, or `CRLF`

- **Include Header Row** (mandatory if `inputFormat` is `CSV`)<br>
  Indicates whether an input CSV string includes a header row containing the column names. (Visible if `inputFormat` is `CSV`.)<br>
  ID: `header` | Type: `boolean` | Default: `true` | Possible values: `true`, `false`

- **Column Names**<br>
  A string specifying the column names as a comma separated list. If `header` is set to `true` this will override the column names specified in the header row of the file. (Visible if `inputFormat` is `CSV`.)<br>
  ID: `colNames` | Type: `string` | Default: none

- **Values for Boolean True**<br>
  A string specifying one value, or a comma separated list of values, that shall be interpreted as boolean `true`. (Visible if `inputFormat` is `CSV`.)<br>
  ID: `trueValues` | Type: `string` | Default: none

- **Values for Boolean False**<br>
  A string specifying one value, or a comma separated list of values, that shall be interpreted as boolean `false`. (Visible if `inputFormat` is `CSV`.)<br>
  ID: `falseValues` | Type: `string` | Default: none

- **Decimal Separator**<br>
  The character that is used in an input CSV string to separate the integer part from the fractional part of a number written in decimal form. (Visible if `inputFormat` is `CSV`.)<br>
  ID: `decSep` | Type: `string` | Default: `.`

- **Thousands Separator**<br>
  A character that is used in an input CSV string to separate groups of digits of a number representing a factor of thousand in front of the decimal separator. (Visible if `inputFormat` is `CSV`.)<br>
  ID: `digitGrpSep` | Type: `string` | Default: none

- **Escape Character**<br>
  A character that is used in an input CSV string to escape characters that would otherwise be interpreted as having a special function. (Visible if `inputFormat` is `CSV`.)<br>
  ID: `escapeChar` | Type: `string` | Default: none

- **Quoting Character**<br>
  The character that is used in an input CSV string to denote the start and end of a quoted item. Column and row separators will be ignored inside quoted items. (Visible if `inputFormat` is `CSV`.)<br>
  ID: `quoteChar` | Type: `string` | Default: ``

- **Datetime Columns**<br>
  A string containing a comma separated list of column names that shall be parsed as date or datetime values. (Visible if `inputFormat` is `CSV`, `JSON`, `JSONLINES`.)<br>
  ID: `dateCols` | Type: `string` | Default: none

- **Ignore Bad Lines**<br>
  Indicates whether to ignore lines in an input CSV string that contain too many columns. If set to `true`, bad lines will be dropped from the output, otherwise an error will be raised. (Visible if `inputFormat` is `CSV`.)<br>
  ID: `ignoreBad` | Type: `boolean` | Default: `false`

- **Format** (mandatory if `inputFormat` is `JSON`)<br>
  The format in which data is represented in an input JSON string. (Visible if `inputFormat` is `JSON`.)
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

## Input

- **binary** (type `scalar`, vtype-id `com.sap.core.binary`)

  Input serialized data. Can be consumed as a stream by this operator if the inputFormat is set to `CSV` or `JSONLINES`. Other formats do not support streaming.

## Output

- **table** (type `table`, vtype-id `*`)

  The input serialized data converted to a table sent as a stream.

- **error** (type `scalar`, vtype-id `com.sap.error`)

  An error that occurred during the conversion.

<br>

