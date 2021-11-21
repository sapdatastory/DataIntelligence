# Oracle vsolution Example

Oracle DB에 액세스 하려면 먼저 Oracle Instant Client를 다운로드 및 등록해야 합니다. <br>

### 1. Create oracle_vsolution
Oracle Instant Client 프로그램(Linux x86-64, Version 12.2.0.1.0)를 다운로드 합니다.<br>
https://www.oracle.com/database/technologies/instant-client/downloads.html
<br>

Instant Client for Linux 영역에서 Instant Client for Linux x86-64를 선택합니다.<br>

![](images/vsol_ora_1.png) <br>

instantclient-basic-linux.x64-12.2.0.1.0.zip 또는 instantclient-basiclite-linux.x64-12.2.0.1.0.zip 를 다운로드 합니다.<br>

![](images/vsol_ora_2.png) <br>


```shell
# 디렉토리
mkdir -p oracle_vsolution/content/files/flowagent
```

```shell
# solution 이름과 버전
vi oracle_vsolution/manifest.json

{
    "name": "vsolution_oracle",
    "version": "1.0.0",
    "format": "2",
    "dependencies": []
}
```

```shell
# Client 프로그램의 압축 풀기 및 파일 링크 설정
unzip instantclient-basic-linux.x64-12.2.0.1.0.zip  -d oracle_vsolution/content/files/flowagent/

cd oracle_vsolution/content/files/flowagent/instantclient_12_2  

ln -s libclntsh.so.12.1 libclntsh.so.12  

ln -s libclntsh.so.12 libclntsh.so

ln -s libclntshcore.so.12.1 libclntshcore.so.12

ln -s libclntshcore.so.12 libclntshcore.so

ln -s libocci.so.12.1 libocci.so.12

ln -s libocci.so.12 libocci.so
```

```shell
# DB 환경변수 설정
vi oracle_vsolution/content/files/flowagent/oracle.properties

ORACLE_INSTANT_CLIENT=./instantclient_12_2
NLS_LANG=AMERICAN_AMERICA.UTF8
```

```shell
# solution 파일 생성
cd oracle_vsoltion

zip -y -r oracle_vsolution.zip ./

ls -F
content/			manifest.json		oracle_vsolution.zip
```


<!--img src="images/jupyter_pipeline4.png" width="550" height="150"/-->

### 2. Import hdliq solution

DI Launchpad -> System Management<br>
Tenant -> Solutions -> '+' button <br>

![](images/vsol_docker_1.png) <br>

hdl_vsolution.zip 파일 선택 <br>

<img src="images/vsol_docker_2.png" width="500" height="250"/> <br>

vsolution_hdliq 확인 <br>

![](images/vsol_docker_3.png)<br>

Tenant -> Strategy -> 'Edit' button <br>

![](images/vsol_docker_4.png)<br>

'+' button <br>

![](images/vsol_docker_5.png)<br>

vsolution_hdliq-1.0.0 선택 <br>

<img src="images/vsol_docker_6.png" width="600" height="400"/> <br>

'Save' button <br>

![](images/vsol_docker_7.png)<br>

### 3. Tenant 환경에서 Dockerfile 확인

Fils -> Union View <br>
files -> vflow -> dockerfiles -> zdemo -> z_hdliq<br>

![](images/vsol_docker_8.png)<br>
![](images/vsol_docker_9.png)<br>

### 4. 사용자 환경에서 Dockerfile 확인

DI Launchpad -> Modeler <br>
Repository -> dockerfiles -> zdemo -> z_hdliq -> Dockerfile <br>

![](images/vsol_docker_10.png)<br>
