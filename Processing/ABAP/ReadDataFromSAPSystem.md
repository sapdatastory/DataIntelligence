`Read Data From SAP System` Operator
=======
com.sap.abap.reader

**Input**<br>
--None--<br>
**Output**<br>
--None--

`Read Data From SAP System` 연산자를 사용하여 ABAP 시스템에서 데이터를 읽을 수 있습니다. 
`Read Data From SAP System` 연산자는 원격 ABAP 시스템에서 선택한 연산자(Operator)에 동적으로 적응합니다.

Note
=======

`Read Data from SAP System` 연산자는 `Snapshot` 기능을 사용합니다. 
이 연산자를 사용하는 그래프를 실행할 때 스냅샷 캡처 옵션이 활성화되어 있는지 확인하십시오. 
그래프를 실행할 때 "Run As" 또는 "Schedule" 옵션에 대해 이 옵션을 활성화해야 합니다.


Configuration parameters
------------

* **ABAP Connection** (required): ABAP 기반 원격 시스템에 대한 연결 정보입니다.
Connection Management에서 미리 정의된 ABAP 연결을 선택할 수 있습니다.

    ID: `connectionID` | Type: `string` | Default: `""`

* **Version** (required): 사용할 연산자의 특정 버전입니다.

    참고: 버전마다 지원하는 기능이 다릅니다. 특정 버전 문서를 보려면 버전을 선택한 후 문서를 다시 엽니다.

    ID: `operatorID` | Type: `string` | Default: `""`

