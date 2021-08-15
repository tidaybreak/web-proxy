#!/bin/sh

cd /opt/app-root/src
if [ ! -d "./venv" ]; then
  virtualenv --no-site-packages venv
fi

source ./venv/bin/activate
  pip install -r requirements.txt


export C_FORCE_ROOT="true"
export LOGFILE="/data/logs"
#file=/data/logs/trading-`date +%Y-%m-%d-%H-%M-%S`
#touch $file

curr_dir=$(pwd)
export PYTHONPATH=${PYTHONPATH}:${curr_dir}
#echo "PYTHONPATH=${PYTHONPATH}" >> $file

nohup python manage.py &
/usr/bin/tail -f logging.log