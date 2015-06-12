# Base docker image
FROM debian:jessie
MAINTAINER François Billant <fbillant@gmail.com>

RUN sed -i.bak 's/jessie main/jessie main contrib non-free/g' /etc/apt/sources.list && \

apt-get update && \
apt-get install -y \
python-lxml python-pip git

RUN cd /root && \
git clone https://github.com/francois-learnings/pyload-autodl.git

RUN cd /root/pyload-autodl && \
pip install -r requirements.txt && \
pip install .

CMD ["/usr/local/bin/autodl"]
