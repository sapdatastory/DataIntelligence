# R Client Operator 사용 방법

com.sap.system.rClient4<br>

Input<br>
--None--<br>
Output<br>
--None--<br>

R Client operator는 Rserve에서 정의한 R 코드를 실행합니다. R 스크립트를 작성하고 미리 정의된 api 객체를 사용하여 callback을 추가하여 실행할 코드를 지정할 수 있습니다. 예를 들어 "input1" 포트에서 새 데이터를 수신할 때 호출되는 callback 함수 myFunc를 설정한 다음 api$setPortCallback(c("input1"), c(" output2"), "myFunc")을 작성하여 "output2" 포트로 데이터를 보낼 수 있습니다.<br>

api 개체가 제공하는 기능은 다음과 같습니다. - api$setPortCallback(inports, outports, functionName) - api$addTimer(period, outports, functionName) - api$setSwitchCallback(inports, outports, functionName) - api$addShutdownHandler(functionName )<br>

이러한 각 기능은 다음에서 설명합니다.<br>

스크립트는 R 클라이언트 연산자를 초기화하는 동안 실행됩니다. 초기화 후에 실행해야 하는 코드의 경우 setPortCallback, addTimer, setSwitchCallback, addShutdownHandler와 같은 api 개체의 메서드를 사용하여 스크립트에서 callback을 추가하고 정의할 수 있습니다.

참고: R Client 연산자는 R 4.1.0으로 구축되었습니다.

## Configuration Parameters
- Switch Start Off: 스위치 콜백이 있는 경우 이 필드가 true이면 그래프 시작부터 다른 콜백이 비활성화됩니다.<br>
ID: switchStartOff | Type: boolean | Default: “true”

- Switch Affects Timer Callbacks: 스위치 콜백이 있는 경우 이 필드가 true이면 타이머 콜백은 스위치 상태의 영향을 받습니다(포트 콜백은 항상 영향을 받습니다).<br>
ID: switchAffectTimerCallbacks | Type: boolean | Default: “true”

- Debug Mode: 기존 외부 Rserve에 연결할 때 더 나은 오류 메시지를 얻으려면 true로 설정하십시오. 활성화하면 성능이 영향을 받을 수 있습니다.<br>
ID: debugMode | Type: boolean | Default: “false”

- Table Name by Outport: 아웃포트 이름에서 테이블 이름으로의 매핑은 데이터 프레임이 지정된 아웃포트로 전송될 때 사용됩니다. configuration에 정의되지 않은 출력에서 데이터 프레임이 전송되면 결과 message.table은 'rclient' + < outportName > 으로 채워진 테이블 이름을 갖게 됩니다.<br>
ID: tableNameByOutport | Type: array | Default: []

## Allowed Types and (Data Pipeline)/R Type Equivalences
### Allowed Types in In/Out Ports
- string
- blob ([]byte)
- float64
- int64
- uint64
- arrays of the types above (for example: []string, [][]float64, etc)
- byte
- message
- any

### (Data Intelligence Modeler)/R Type Equivalences
|**Data Intelligence Modeler**|**R**|
|:-----|:-----|
|string|character|
|blob|raw|
|float64|double/numeric (64 bits)|
|int64|integer (signed 32 bits)|
|uint64|integer (signed 32 bits)|
|slice or array|vector|
|byte|integer (signed 32 bits)|
|message*|list(Body,Attributes,Encoding)|
|message.table**|data frame|

|* 필드 인코딩이 'table'과 다른 메시지. R에서 메시지 생성의 예: m <- list(Body=11, Attributes=list(field1="foo"), Encoding="bar").|
|---|
|** 필드 인코딩이 'table'인 메시지. R에서는 data frame으로 표현됩니다.|

참고: R Client 연산자는 Go와 R 간의 숫자 변환 중에 데이터 손실이 발생하는 경우 경고 또는 오류가 발생하지 않습니다. 예를 들어, 일부 uint64 값은 R에서 double 또는 integer로 표시될 수 없습니다. R 클라이언트는 이러한 경우의 결과를 지정하지 않습니다.<br>

참고: complex number, matrix, factor와 같은 일부 R 유형은 Modeler 및 R 변환 중에 지원되지 않습니다. R Client 출력 포트에서 전송하면 때때로 오류가 발생하지 않을 수 있지만 결과는 정의되지 않습니다.<br>

이 섹션에 표시된 table는 operator의 포트에서 직접 사용할 수 있는 유형만 다룹니다. message 데이터 유형의 내부 필드에서 사용할 수 있는 유형과 관련된 자세한 정보는 Go/R Type Equivalences and Conversions 섹션에서 볼 수 있습니다.

```shell
```

