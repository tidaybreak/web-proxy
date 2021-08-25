#!/bin/sh

curr_dir=$(pwd)
chmod 777 $curr_dir

docker stop web-proxy-$1
docker rm web-proxy-$1
docker run --name web-proxy-$1 -d \
--restart=always \
-e TERM=linux \
-e APP_CONFIG=$1 \
--net mynet \
-p $2:8080 \
--mount type=bind,source=/etc/resolv.conf,target=/etc/resolv.conf \
--mount type=bind,source=$curr_dir,target=/opt/app-root/src \
centos/python-36-centos7:latest \
/bin/sh /opt/app-root/src/run.sh