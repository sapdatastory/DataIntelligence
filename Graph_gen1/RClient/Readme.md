RClient Operator 처리 예제
===

# 1. File to File 처리
## 1.1 Read File Operator : message.file <-> message <-> message.file
![](images/1.FilePython.png)<br>
Read File --> From File --> RClinet --> To File --> Write File --> Graph Terminator

```R
msg2df <- function(msg) {
    csv <- rawToChar(msg$Body)
    df <- read.csv(text=csv, encoding="UTF-8", header=TRUE, stringsAsFactors=FALSE)
}

df2msg <- function(df) {
    conn <- rawConnection(raw(0), "w")
    write.csv(df, conn, row.names = FALSE)
    csv <- rawConnectionValue(conn)
    close(conn)
    
    numRows <- nrow(df)
    attributes <- list(numRows=numRows)
    msg <- list(Body=csv, Attributes=attributes, Encoding="string")
}

processData <- function(df) {
#   implement your data processing logic here:
    df <- subset(df, CATEGORY == "Notebooks", select=c("PRODUCTID", "PRODUCTNAME", "CATEGORY"))
}

onInput <- function(msg) {
    df <- msg2df(msg)
    result <- processData(df)
    outMsg <- df2msg(result)
    list(outData=outMsg)
}

api$setPortCallback(c("inData"), c("outData"), "onInput")
```
# 2. File to DB 처리
## 2.1 Read File Operator : message.file <-> message <-> message
![](images/1.FilePython.png)<br>
Read File --> From File --> RClient --> HANA Client --> Graph Terminator

```R
msg2df <- function(msg) {
    csv <- rawToChar(msg$Body)
    df <- read.csv(text=csv, encoding="UTF-8", header=TRUE, stringsAsFactors=FALSE)
}

df2msg <- function(df) {
    conn <- rawConnection(raw(0), "w")
    write.csv(df, conn, row.names = FALSE)
    csv <- rawConnectionValue(conn)
    close(conn)

    numRows <- nrow(df)
    attributes <- list(numRows=numRows)
    msg <- list(Body=csv, Attributes=attributes, Encoding="bar")
}

processData <- function(df) {
#   implement your data processing logic here:
    df <- subset(df, CATEGORY == "Notebooks", select=c("PRODUCTID", "PRODUCTNAME", "CATEGORY"))
}

onInput <- function(msg) {
    df <- msg2df(msg)
    result <- processData(df)
    outMsg <- df2msg(result)
    list(outData=outMsg)
}

api$setPortCallback(c("inData"), c("outData"), "onInput")
```

# 3. DB to File 처리
## 3.1 HANA Client Operator : message <-> message <-> message.file
![](images/1.FilePython.png)<br>
Constant Generator --> HANA Client --> RClient --> To File --> Write File --> Graph Terminator

```R

```

# 4. DB to DB 처리
## 4.1 HANA Client Operator : message <-> message <-> message
![](images/1.FilePython.png)<br>
Constant Generator --> HANA Client --> RClient --> HANA Client --> Graph Terminator

```R

```
