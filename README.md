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
* optional: create a virtualenv before running the step below
* pip install -r requirements/compiled.txt
* Add a settings_local.py file from settings_local.py-dist

Please refer to [Playdoh's docs][github-playdoh] for more information.

[github-playdoh]: http://mozilla.github.com/playdoh
[github-spark]: http://mozilla.github.com/spark
[github-sparklib]: http://mozilla.github.com/spark-lib
