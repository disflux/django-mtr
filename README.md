### Warning: THIS SOFTWARE IS ALPHA, IT IS NOT PRODUCTION READY AT THIS TIME

Django-MTR
==========
Derek Musselmann - May 2013

Overview
--------
django-mtr is a Material Test Report document management application aimed
primarily at fastener distributors. It contains modules for tracking documents,
generating labels, generating mtr packets for customers, vendor tracking, part
number tracking, and specification lookup and tracking. Reports can be attached
to customer orders, searchable by work order number, customer po number, lot
number, heat number, and other data.

An unlimited number of user defined documents can be attached to each report.

Requirements
------------
See ```requirements.txt``` for all python requirements.  

* Django 1.5+
* PostgreSQL 9.0+
* An Amazon AWS account and S3 bucket

Setup
-----
1. Checkout this repository (```git clone https://github.com/phrac/django-mtr.git```)
2. Setup an AWS account and S3 bucket
3. Copy ```mtr/settings_local-template.py``` to ```mtr/settings_local.py``` and edit accordingly
4. Edit ```mtr/settings.py``` accordingly
5. run ```manage.py syncdb``` to populate database tables
6. Deploy via wsgi or run the development server for testing

