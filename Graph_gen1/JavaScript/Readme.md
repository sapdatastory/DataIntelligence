JS Operator 처리 예제
===

# 1. File to File 처리
## 1.1 Read File Operator : message.file <-> message <-> message.file
![](images/1.FilePython.png)<br>
Read File --> From File --> JS --> To File --> Write File --> Graph Terminator

```javascript
$.setPortCallback("inData", onInput);

function processData(data) {
//  implement your data processing logic here:
    var result = [];
    var dataCols = Object.keys(data[0]).filter(function(c) { return c !== "id"; });

    data.forEach(function(o, i) {
        result.push(o);

        if (i < data.length - 1) {
            var o_inter = { id: o.id + "_" + data[i + 1].id };

            dataCols.forEach(function(c) {
                o_inter[c] = parseFloat(o[c]) + 0.5 * (parseFloat(data[i + 1][c]) - parseFloat(o[c]));
            });

            result.push(o_inter);
        }

    });

    return result;
}

function onInput(ctx, msg) {
    var outMsg = $.copyMessage(msg);
    var data = JSON.parse(String.fromCharCode.apply(null, msg.Body));
    var result = processData(data);
    outMsg.Body = result;
    $.outData(outMsg);
}
```
# 2. File to DB 처리
## 2.1 Read File Operator : message.file <-> message <-> message
![](images/1.FilePython.png)<br>
Read File --> From File --> JS --> HANA Client --> Graph Terminator

```javascript
$.setPortCallback("inData", onInput);

function processData(data) {
//  implement your data processing logic here:
    var result = [];
    var dataCols = Object.keys(data[0]).filter(function(c) { return c !== "id"; });

    var tmp = data.map(function(o) {
        var r = { id: o.id };
        dataCols.forEach(function(c) { r[c] = parseFloat(o[c]); });
        return r;
    });

    result = tmp.concat(tmp.slice(1).map(function(o, i) {
        var o_inter = { id: tmp[i].id + "_" + o.id };

        dataCols.forEach(function(c) {
            o_inter[c] = o[c] + 0.5 * (tmp[i][c] - o[c]);
        });

        return o_inter;
    }));

    return result;
}

function onInput(ctx, msg) {
    var outMsg = $.copyMessage(msg);
    var data = JSON.parse(String.fromCharCode.apply(null, msg.Body));
    var result = processData(data);
    outMsg.Body = result;
    $.outData(outMsg);
}
```

# 3. DB to File 처리
## 3.1 HANA Client Operator : message <-> message <-> message.file
![](images/1.FilePython.png)<br>
Constant Generator --> HANA Client --> JS --> To File --> Write File --> Graph Terminator

```javascript
$.setPortCallback("inData", onInput);

function processData(data) {
//  implement your data processing logic here:
    var result = [];
    var dataCols = Object.keys(data[0]).filter(function(c) { return c !== "ID"; });

    data.forEach(function(o, i) {
        result.push(o);

        if (i < data.length - 1) {
            var o_inter = { ID: o.ID + "_" + data[i + 1].ID };

            dataCols.forEach(function(c) {
                o_inter[c] = parseFloat(o[c]) + 0.5 * (parseFloat(data[i + 1][c]) - parseFloat(o[c]));
            });

            result.push(o_inter);
        }

    });

    return result;
}

function onInput(ctx, msg) {
    var outMsg = $.copyMessage(msg);
    var result = processData(msg.Body);
    outMsg.Body = result;
    $.outData(outMsg);
}
```
