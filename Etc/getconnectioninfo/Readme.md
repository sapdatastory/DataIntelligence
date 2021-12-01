get_connection_info
=====
```python
import requests
connectionId = 'S4'
connection_content = requests.get("http://vsystem-internal:8796/app/datahub-app-connection/connectionsFull/%s" % connectionId).content
connection_content
```
