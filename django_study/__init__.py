import pymysql

pymysql.install_as_MySQLdb()
# anaconda3/envs/study_django/lib/python3.7/site-packages/django/db/backends/mysql/base.py
# if version < (1, 3, 13):
#     pass
#     raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
