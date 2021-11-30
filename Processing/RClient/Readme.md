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

- Table Name by Outport: 아웃포트 이름에서 테이블 이름으로의 매핑은 데이터 프레임이 지정된 아웃포트로 전송될 때 사용됩니다. configuration에 정의되지 않은 출력에서 데이터 프레임이 전송되면 결과 message.table은 'rclient' + <outportName>으로 채워진 테이블 이름을 갖게 됩니다.<br>
ID: tableNameByOutport | Type: array | Default: []

## Configuration Parameters

```shell


```

