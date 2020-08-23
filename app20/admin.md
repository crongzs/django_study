# Django Admin

##### 使admin中文显示的配置
settings.py
~~~python
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# 如果USE_TZ设置为False，那么Django获取到的时间就是一个 navie time 类型的时间
USE_TZ = False
~~~

##### 将app注册到admin
app20/admin.py
~~~python
from django.contrib import admin

# Register your models here.

from app20.models import Article, Author, Category, Book, BookOrder, Publish


# 给Article表创建一个管理器
class ArticleModelAdmin(admin.ModelAdmin):
    pass


# 将管理器注册进admin
admin.site.register(Article, ArticleModelAdmin)
~~~

##### 给app定义一个名称
app20/apps.py
~~~python
from django.apps import AppConfig


class App20Config(AppConfig):
    name = 'app20'
    verbose_name = 'Admin管理'
~~~