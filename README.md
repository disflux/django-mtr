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

Features
--------
* Search by any data, including heat number, lot number, PO number, work order number
* Generate barcoded product labels automatically
* Generate in-house material test reports
* Generate inspection reports pre-filled with product data
* Email/fax documents
* Generate MTR report packets for customers
* Documents stored in Amazon S3 buckets
* Management commands for easy database backups
* Complete audit trail that tracks document attachments, report creation, deletions, changes, etc
* Attach unlimited documents to reports
* Link reports together (ex: a manufactured product would link to the raw material)
* User defined document types (Mill test reports, plating certifications, etc.)
* Batch inspection report creation
* Copy report to new reports
* Part editor

Requirements
------------
See ```requirements.txt``` for all python requirements.  

* Django 1.5+
* PostgreSQL 9.0+
* An Amazon AWS account and S3 bucket
* Whoosh (for search)

Setup
-----
1. Checkout this repository (```git clone https://github.com/phrac/django-mtr.git```)
2. Setup an AWS account and S3 bucket
3. Copy ```mtr/settings_local-template.py``` to ```mtr/settings_local.py``` and edit accordingly
4. Edit ```mtr/settings.py``` accordingly
5. run ```manage.py syncdb``` to populate database tables
6. Deploy via wsgi or run the development server for testing

Screenshots
-----------
* Dashboard
![dashboard](https://raw.github.com/phrac/django-mtr/master/dashboard.png)
* Report
![report](https://raw.github.com/phrac/django-mtr/master/report.png)
* New Report
![report](https://raw.github.com/phrac/django-mtr/master/new_report.png)
* Search Results
![search](https://raw.github.com/phrac/django-mtr/master/search.png)
* Product Labels (pdf)
![search](https://raw.github.com/phrac/django-mtr/master/label.png)

