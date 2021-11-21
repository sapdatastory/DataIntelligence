# hdliq dockerfile vsolution Example

### 1. Create hdliq_vsolution

```shell
mkdir -p hdliq_vsolution/content/files/vflow/dockerfiles/zdemo/z_hdliq
```

```shell
cp Dockerfile hdliq_vsolution/content/files/vflow/dockerfiles/zdemo/z_hdliq

cp Tags.json hdliq_vsolution/content/files/vflow/dockerfiles/zdemo/z_hdliq

cp iq171.TGZ hdliq_vsolution/content/files/vflow/dockerfiles/zdemo/z_hdliq
```

```shell
vi hdliq_vsoltion/manifest.json
{
    "name": "vsolution_hdliq",
    "version": "1.0.0",
    "format": "2",
    "dependencies": []
}
```

```shell
cd hdliq_vsoltion

zip -r hdliq_vsolution.zip ./

ls -F
content/		hdliq_vsolution.zip	    manifest.json
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

Add Solutions -> '+' Button <br>

![](images/vsol_docker_5.png)<br>

![](images/vsol_docker_6.png)<br>

![](images/vsol_docker_7.png)<br>

![](images/vsol_docker_8.png)<br>

![](images/vsol_docker_9.png)<br>

![](images/vsol_docker_10.png)<br>

