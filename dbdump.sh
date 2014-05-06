#!/bin/bash
cd /home/tsaderek/webapps/djangomtr
source ~/.virtualenvs/django-mtr/bin/activate
cd django-mtr
./manage.py make_dump default
deactivate

