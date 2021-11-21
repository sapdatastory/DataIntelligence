# DB2 vsolution Example

DB2 DB에 액세스 하려면 먼저 IBM Data Server Driver for ODBC and CLI (CLI Driver)를 다운로드 및 등록해야 합니다. <br>


### 1. Create db2_vsolution
MySQL ODBC Connector 프로그램(Version 8.0.12, Linux - Generic (glibc 2.12)(x86,64-bit))를 다운로드 합니다.<br>
https://downloads.mysql.com/archives/c-odbc/
<br>

버전은 반드시 8.0.12를 선택합니다. 다른 버전 선택 시 연결 이슈가 발생할 수도 있습니다. <br>
v10.1fp6_linuxx64_odbc_cli.tar.gz 를 다운로드 합니다.<br>

![](images/vsol_db2_1.png) <br>

```shell
# 디렉토리
mkdir -p db2_vsolution/content/files/flowagent
```

```shell
# solution 이름과 버전
vi db2_vsolution/manifest.json

{
    "name": "vsolution_db2",
    "version": "1.0.0",
    "format": "2",
    "dependencies": []
}
```

```shell
# Client 프로그램의 압축 풀기 및 파일 링크 설정
tar -xvzf ibm-db2-odbc-<VERSION>.tar.gz -C db2_vsolution/content/files/flowagent
```

```shell
# DB 환경변수 설정
vi db2_vsolution/content/files/flowagent/db2.properties

DB2_CLI_DRIVER=./clidriver/lib
```

```shell
# solution 파일 생성
cd db2_vsoltion

zip -r db2_vsolution.zip ./

ls -F
content/		db2_vsolution.zip	manifest.json
```


### 2. Import db2 solution

DI Launchpad -> System Management<br>
Tenant -> Solutions -> '+' button <br>

![](images/vsol_db2_2.png) <br>

db2_vsolution.zip 파일 선택 <br>

vsolution_db2 확인 <br>


Tenant -> Strategy -> 'Edit' button <br>

![](images/vsol_db2_3.png)<br>

'+' button <br>

![](images/vsol_db2_4.png)<br>

vsolution_db2-1.0.0 선택 <br>

'Save' button <br>


### 3. Restart flowagent

DI Launchpad -> System Management<br>
Applications -> 'flowagent' Search -> Restart Icon <br>

![](images/vsol_db2_5.png)<br>


### 4. Tenant 환경에서 flowagent 확인

Fils -> Union View <br>
files -> flowagent -> clidriver 디렉토리, db2.properties 파일 <br>

![](images/vsol_db2_6.png)<br>
