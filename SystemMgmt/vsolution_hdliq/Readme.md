# hdliq dockerfile vsolution Example

### Create hdliq vsolution

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

### import hdliq vsolution



