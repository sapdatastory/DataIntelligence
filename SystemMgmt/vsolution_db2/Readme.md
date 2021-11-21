# DB2 vsolution Example

DB2 DB에 액세스 하려면 먼저 IBM Data Server Driver for ODBC and CLI (CLI Driver)를 다운로드 및 등록해야 합니다. <br>


### 1. Create mysql_vsolution
MySQL ODBC Connector 프로그램(Version 8.0.12, Linux - Generic (glibc 2.12)(x86,64-bit))를 다운로드 합니다.<br>
https://downloads.mysql.com/archives/c-odbc/
<br>

버전은 반드시 8.0.12를 선택합니다. 다른 버전 선택 시 연결 이슈가 발생할 수도 있습니다. <br>
v10.1fp6_linuxx64_odbc_cli.tar.gz 를 다운로드 합니다.<br>

![](images/vsol_mysql_1.png) <br>

```shell
# 디렉토리
mkdir -p mysql_vsolution/content/files/flowagent
```

```shell
# solution 이름과 버전
vi mysql_vsolution/manifest.json

{
    "name": "vsolution_mysql",
    "version": "1.0.0",
    "format": "2",
    "dependencies": []
}
```

```shell
# Client 프로그램의 압축 풀기 및 파일 링크 설정
tar -xvzf mysql-connector-odbc-8.0.12-linux-glibc2.12-x86-64bit.tar.gz -C mysql_vsolution/content/files/flowagent/
```

```shell
# DB 환경변수 설정
vi mysql_vsolution/content/files/flowagent/mysql.properties

MYSQL_DRIVERMANAGER=./mysql-connector-odbc-8.0.12-linux-glibc2.12-x86-64bit/lib/libmyodbc8w.so
```

```shell
# solution 파일 생성
cd mysql_vsoltion

zip -r mysql_vsolution.zip ./

ls -F
content/		manifest.json		mysql_vsolution.zip
```


### 2. Import mysql solution

DI Launchpad -> System Management<br>
Tenant -> Solutions -> '+' button <br>

![](images/vsol_mysql_2.png) <br>

mysql_vsolution.zip 파일 선택 <br>

vsolution_mysql 확인 <br>


Tenant -> Strategy -> 'Edit' button <br>

![](images/vsol_mysql_3.png)<br>

'+' button <br>

![](images/vsol_mysql_4.png)<br>

vsolution_mysql-1.0.0 선택 <br>

'Save' button <br>


### 3. Restart flowagent

DI Launchpad -> System Management<br>
Applications -> 'flowagent' Search -> Restart Icon <br>

![](images/vsol_mysql_5.png)<br>


### 4. Tenant 환경에서 flowagent 확인

Fils -> Union View <br>
files -> flowagent -> mysql-connector-odbc-8.0.12-linux-glibc2.12-x86-64bit 디렉토리, mysql.properties 파일 <br>

![](images/vsol_mysql_6.png)<br>

