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

## 기본 예제

```shell


```
