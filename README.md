Spark
=====

Spark desktop and mobile campaign websites.


Based off Mozilla's [Playdoh][github-playdoh] web application template,
Spark is [hosted on github][github-spark]. 

Python dependencies are in the spark-lib repository also hosted on [github][github-sparklib].


Installation steps
==================

Important: clone into a directory with a different name than spark,
or else there will be a conflict with a django app named spark.

* git clone --recursive git://github.com/mozilla/spark.git my_spark
* Optional: create a virtualenv before running the step below
* pip install -r requirements/compiled.txt
* cp settings_local.py-dist settings_local.py
* Create the database configured in settings_local.py
* ./vendor/src/schematic/schematic migrations/
* From mysql: source lib/staging/test-data.sql
* ./manage.py runserver

Please refer to [Playdoh's docs][github-playdoh] for more information.

[github-playdoh]: http://github.com/mozilla/playdoh
[github-spark]: http://github.com/mozilla/spark
[github-sparklib]: http://github.com/mozilla/spark-lib


Desktop and mobile versions
===========================

When the installation is complete:

* Desktop website of Spark: http://localhost:8000/
* Mobile Spark game: http://localhost:8000/m/