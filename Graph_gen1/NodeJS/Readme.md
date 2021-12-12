Node.js Operator 처리 예제
===

# 1. File to File 처리
## 1.1 Read File Operator : message.file <-> message <-> message.file
![](images/1.FilePython.png)<br>
Read File --> From File --> Node.js --> To File --> Write File --> Graph Terminator

```javascript
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

# 2. File to DB 처리
## 2.1 Read File Operator : message.file <-> message <-> message
![](images/1.FilePython.png)<br>
Read File --> From File --> Node.js --> HANA Client --> Graph Terminator

```javascript

```

# 3. DB to File 처리
## 3.1 HANA Client Operator : message <-> message <-> message.file
![](images/1.FilePython.png)<br>
Constant Generator --> HANA Client --> Node.js --> To File --> Write File --> Graph Terminator

```javascript

```

# 4. DB to DB 처리
## 3.1 HANA Client Operator : message <-> message <-> message
![](images/1.FilePython.png)<br>
Constant Generator --> HANA Client --> Node.js --> HANA Client --> Graph Terminator

```javascript

```
