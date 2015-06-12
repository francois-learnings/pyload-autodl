# pyload autodl
## Install
### Docker
#### Run
```
docker run -ti --rm -v ~/autodl_config.json:/etc/autodl/audl_config.json francois/pyload-autodl:latest
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

tests specific requirements:
phantomjs to test jherbergNet plugin

```
apt-get install -y python-lxml python-pip
git clone https://github.com/francois-learnings/pyload-autodl.git
cd pyload-autodl
pip install -r requirements.txt
autodl
```

TOOD: A lot...
