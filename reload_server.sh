#!/bin/bash
set -e

source env/bin/activate

flake8 .

pip install -r requirements.txt
(cd dashboard/static; npm install; grunt build)

pid_file="$HOME/tmp/dash_stats_g.pid"
if [ -f "$pid_file" ]
then
	echo "KILL gunicorn"
	cat $pid_file | xargs kill
	echo "Waiting....";
	for i in {5..1}
	do
		echo $i
		sleep 1
	done
fi
echo "starting gunicorn"
gunicorn -c gunicorn_conf.py run:app

echo "started"
