Node.js Base Operator
=======
이 연산자는 Node.js를 기반으로 하는 ECMAScript 2015(ES6)의 사용자 지정 스크립트를 지원합니다.
현재 사용 중인 버전은 v8.11.4 이상입니다.

Note:
------
modeler에서는 추가적인 3rd-party node-module을 추가할 수 없습니다.
이 연산자는 __@sap/vflow-sub-node-sdk__ 로 제한됩니다.

다른 모듈은 작동하거나 또는 작동하지 않을 수 있지만 이것을 보장하지 않습니다.

원하는 것을 사용하여 완전한 기능을 갖춘 Node.js 개발을 위해 외부 개발 프로젝트를 만드십시오.
외부에서 생성된 운영자는 vsolution 아카이브로 배포할 수 있습니다.

세부 정보 참조: [help.sap.com](https://help.sap.com/viewer/product/SAP_DATA_INTELLIGENCE/)

---

- None

Input
---

- None

Output
---

- None

Examples
---
```shell
const SDK = require("@sap/vflow-sub-node-sdk")
const op = SDK.Operator.getInstance()

const processData = data => {
    //  implement your data processing logic here:
    let result = []
    const dataCols = Object.keys(data[0]).filter(c => c !== "id")

    data.forEach((o, i) => {
        result.push(o)

        if (i < data.length - 1) {

            const o_inter = dataCols.reduce((o_i, c) => {
                o_i[c] = parseFloat(o[c]) + 0.5 * (parseFloat(data[i + 1][c]) - parseFloat(o[c]))
                return o_i
            }, { id: o.id + "_" + data[i + 1].id })

            result.push(o_inter)
        }

    })

    return result
}

const handleMsg = msg => {
    const data = JSON.parse(String.fromCharCode.apply(null, msg.Body))
    const result = processData(data)
    op.outData({ Attributes: msg.Attributes, Body: result });
}

op.inData.onInput(handleMsg)
```
```shell
const Papa = require("papaparse")
const SDK = require("@sap/vflow-sub-node-sdk")

const op = SDK.Operator.getInstance()
let keyProp = ""
let colSep = ""
let rowSep = ""

const parseCsv = (csv, col, row, key) => {
    colSep = col === "unkown" ? "" : col

    rowSep = row === "unkown" ? "" :
        row === "CR" ? "\r" : 
        row === "LF" ? "\n" : 
        row === "CRLF" ? "\r\n" : ""

    const parsed = Papa.parse(csv, { 
        delimiter: colSep,
        newline: rowSep,
        skipEmptyLines: "greedy",
        header: true
    })

    if (col === "unkown") colSep = parsed.meta.delimiter
    if (row === "unkown") rowSep = parsed.meta.linebreak
    
    let data = []
    const errors = parsed.meta.errors || []

    if (parsed.meta.fields.includes(key)) {
        keyProp = key

        data = parsed.data.map(row => Object.keys(row).reduce((r, c) => {
            if (c !== keyProp) r[c] = parseFloat(r[c]) == r[c] ? parseFloat(r[c]) : r[c]
            return r
        }, row))

    } else {
        // re-use Papa's error structure

        errors.push({
            type: "FieldMismatch",
            code: "KeyNotFound",
            message: "Key property not found in input header fields",
            row: 0
        })

    }

    return { data, errors }
}

const stringifyResult = res => res.length === 0 ? "" : "" + 
    // header row
    Object.keys(res[0]).join(colSep) + rowSep +     
    // data rows + final row separator
    res.map(row => Object.values(row).join(colSep)).join(rowSep) + rowSep

const processData = data => {
    // implement your data processing logic here:
    const result = []

    if (keyProp !== "" && data.length > 1) {
        const dataCols = Object.keys(data[0]).filter(d => d !== keyProp)

        data.forEach((d, i) => {
            result.push(d)
    
            if (i < data.length - 1) {
                const d_inter = {}
                d_inter[keyProp] =  d[keyProp] + "__" + data[i + 1][keyProp]
    
                dataCols.forEach(c => {

                    if (typeof d[c] === "number") {
                        d_inter[c] = d[c] + 0.5 * (data[i + 1][c] - d[c])
                    } else {
                        d_inter[c] = d[c]
                    }

                })
    
                result.push(d_inter)
            }
    
        })

    }
    
    return result
}

const handle = msg => {
    let csv = ""
    
    if (msg.Encoding === "blob") {
        csv = String.fromCharCode(...msg.Body)
    } else {
        csv = msg.Body
    }
    
    const parsed = parseCsv(csv, op.config.colSeparator, op.config.rowSeparator, op.config.keyProperty)
    if (parsed.errors.length > 0) op.outError(parsed.errors)
    const result = processData(parsed.data)
    csv = stringifyResult(result)

    op.outData({ Attributes: msg.Attributes, Encoding: "string", Body: csv })
}

op.inData.onInput(handle)

// enable unit testing
module.exports = { parseCsv, stringifyResult, processData, handle }
```
