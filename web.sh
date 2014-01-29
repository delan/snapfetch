#!/bin/sh
sudo gunicorn -w 8 -b 0.0.0.0:80 \
	--access-logfile - \
	--access-logformat '%(p)s %(s)s %(r)s' \
	"$@" web:app
