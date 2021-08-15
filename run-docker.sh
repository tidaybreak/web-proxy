#!/bin/sh

docker stop web-proxy
docker rm web-proxy
docker run --name web-proxy -d \
--restart=always \
-e PYTHONUNBUFFERED=1 \
-e TERM=linux \
-e C_FORCE_ROOT=true \
-e APP_CONFIG= $1 \
--net mynet \
--ip 172.18.0.135 \
-p 80:5000 \
--mount type=bind,source=/etc/resolv.conf,target=/etc/resolv.conf \
--mount type=bind,source=/home/data/docker-volume/web-proxy/,target=/opt/app-root/src \
centos/python-36-centos7:latest \
/bin/sh /opt/app-root/src/run.sh