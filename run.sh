#!/bin/sh
[ ! -z $BIND_ADDRESS ] && bind_params="-b $BIND_ADDRESS"
gunicorn app:app -n castestor -w 3 --max-requests 10000 --timeout 60 $bind_params

