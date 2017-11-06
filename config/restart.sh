#!/bin/bash
service supervisor stop && kill -9 $(ps -e|grep uwsgi |awk '{print $1}') && service supervisor start
