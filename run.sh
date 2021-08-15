#!/bin/sh

cd /opt/app-root/src
if [ ! -d "/venv" ]; then
  virtualenv --no-site-packages venv
fi

export C_FORCE_ROOT="true"
export LOGFILE="/data/logs"
#file=/data/logs/trading-`date +%Y-%m-%d-%H-%M-%S`
#touch $file

source ./venv/bin/activate

curr_dir=$(pwd)
export PYTHONPATH=${PYTHONPATH}:${curr_dir}
#echo "PYTHONPATH=${PYTHONPATH}" >> $file

nohup python manage.py
#/usr/bin/tail -f $file