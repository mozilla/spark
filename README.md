Spark
=====

Spark desktop and mobile campaign websites.


Based off Mozilla's [Playdoh][github-playdoh] web application template,
Spark is [hosted on github][github-spark]. 

Python dependencies are in the spark-lib repository also hosted on [github][github-sparklib].

Please refer to [Playdoh's docs][github-playdoh] for more information.

[github-playdoh]: http://github.com/mozilla/playdoh
[github-spark]: http://github.com/mozilla/spark
[github-sparklib]: http://github.com/mozilla/spark-lib


Getting started (all environments)
==================================

Important: clone into a directory with a different name than spark,
or else there will be a conflict with a django app named spark.

* git clone --recursive git://github.com/mozilla/spark.git my_spark
* Optional: create a virtualenv before running the step below
* pip install -r requirements/compiled.txt


Dev installation
================

* Refer to 'Getting started' above
* cp settings_local.py-dev settings_local.py
* Configure the database in settings_local.py
* ./vendor/src/schematic/schematic migrations/ 
* ./manage.py runserver

* Enabling Celery tasks: ./manage.py celeryd
* For optional test data, run from mysql: source lib/staging/test-data.sql

When the dev installation is complete:
Access desktop version: http://localhost:8000/
Accessing mobile version: http://localhost:8000/m/


Stage installation
==================

* Refer to 'Getting started' above
* cp settings_local.py-dist settings_local.py
* Configure all required settings in settings_local.py for stage
* Import test data in mysql: source lib/staging/test-data.sql
* Set up the Celery server (Celery settings are in settings.py)
* run celeryd


Production installation
=======================

* Refer to 'Getting started' above
* cp settings_local.py-dist settings_local.py
* Configure all required settings in settings_local.py for production
* Set up the Celery server (Celery settings are in settings.py)
* run celeryd

