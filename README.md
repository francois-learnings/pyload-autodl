# pyload autodl
## Install
### Docker
#### Run
```
docker run -ti --rm -v ~/autodl:/etc/autodl -e CONFIG_FILE=/etc/autodl/config.json -e USER_SETTINGS_FILE=/etc/autodl/user_settings.json -e  SERVER_IP=<xxx.xxx.xxx.xxx> -e SERVER_PORT=8000 -e USER=<pyload_user> -e PASSWORD=<pyload_user_password> francois/pyload-autodl:latest
```
#### Build
```
git clone https://github.com/francois-learnings/pyload-autodl.git
cd pyload-autodl
docker build -t francois/pyload-autodl .
```

### Sources
requirements:
    - lxml

plugins specific requirments:
    - jhebgerNet plugin require "phantomjs"
    - horriblesubsInfo require "phantomjs"

tests specific requirements:
phantomjs to test jherbergNet plugin

```
apt-get install -y python-lxml python-pip
git clone https://github.com/francois-learnings/pyload-autodl.git
cd pyload-autodl
pip install -r requirements.txt
```
Run:
- with arguments :
```
autodl -c /path/to/config_file.json -s /path/to/user_settings.json -a pyload_server_ip_address -u pyload_user -p pyload_user_password -P pyload_port
```

- with environment variables:
```
export CONFIG_FILE=
export USER_SETTINGS_FILE=
export SERVER_IP=
export SERVER_PORT=
export USER=
export PASSWORD=

autodl
```

TOOD: A lot...
