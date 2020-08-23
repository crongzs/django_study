# Django数据库

* django连接mysql数据库报错Did you install mysqlclient?

解决：

pip install mysqlclient

pip install pymysql

在项目 __init__.py文件下添加如下代码

~~~python
import pymysql

pymysql.install_as_MySQLdb()
~~~

注释pymysql依赖包中的版本要求信息

~~~python
# anaconda3/envs/study_django/lib/python3.7/site-packages/django/db/backends/mysql/base.py
# if version < (1, 3, 13):
#     pass
#     raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
~~~

### 在Django中操作数据库

在`Django`中操作数据库有两种方式。第一种方式就是使用原生`sql`语句操作，第二种就是使用`ORM`模型来操作，现在使用第一种。

在`Django`中使用原生`sql`语句操作其实就是使用`python db api`的接口来操作。如果你的`mysql`驱动使用的是`pymysql`，那么你就是使用`pymysql`来操作的，只不过`Django`将数据库连接的这一部分封装好了，我们只要在`settings.py`中配置好了数据库连接信息后直接使用`Django`封装好的接口就可以操作了

app3/views.py

~~~python
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

from django.db import connection


# ------------------ Django操作数据库 ------------------
def to_do_sql(request):
    ''' Django 使用原生 sql 语句操作数据库 '''

    cursor = connection.cursor()

    # execute() 执行sql语句
    # cursor.execute("insert into sql_book(id, name, author) values (null, '三国演义', '罗贯中')")
    cursor.execute("select * from sql_book")

    # fetchone 执行了查询操作后 获取第一条数据
    # rows = cursor.fetchone()
    # fetchall 执行了查询操作后 获取所有数据
    rows = cursor.fetchall()
    # fetchmany(size) 在执行查询操作以后，获取多条数据。具体是多少条要看传的size参数。如果不传size参数，那么默认是获取第一条数据

    for row in rows:
        print(row)
    # (None, '三国演义', '罗贯中')

    context = {}

    return render(request, 'app3/app3-1Django使用原生sql.html', context=context)

~~~

app3/urls.py

~~~python
from django.urls import path

from app3 import views

app_name = 'app3'

urlpatterns = [
    # Django 使用原生 sql 语句操作数据库
    path('sql/', views.to_do_sql, name='app3-1'),
]

~~~

##### Python DB API下规范下cursor对象常用接口：

1. `description`：如果`cursor`执行了查询的`sql`代码。那么读取`cursor.description`属性的时候，将返回一个列表，这个列表中装的是元组，元组中装的分别是`(name,type_code,display_size,internal_size,precision,scale,null_ok)`，其中`name`代表的是查找出来的数据的字段名称，其他参数暂时用处不大。

2. `rowcount`：代表的是在执行了`sql`语句后受影响的行数。

3. `close`：关闭游标。关闭游标以后就再也不能使用了，否则会抛出异常。

4. `execute(sql[,parameters])`：执行某个`sql`语句。如果在执行`sql`语句的时候还需要传递参数，那么可以传给`parameters`参数。示例代码如下：

   ```python
    cursor.execute("select * from article where id=%s",(1,))
   ```

5. `fetchone`：在执行了查询操作以后，获取第一条数据。

6. `fetchmany(size)`：在执行查询操作以后，获取多条数据。具体是多少条要看传的`size`参数。如果不传`size`参数，那么默认是获取第一条数据。

7. `fetchall`：获取所有满足`sql`语句的数据。

### 创建ORM模型

`ORM`模型一般都是放在`app`的`models.py`文件中。每个`app`都可以拥有自己的模型。并且如果这个模型想要映射到数据库中，那么这个`app`必须要放在`settings.py`的`INSTALLED_APP`中进行安装。

### 映射模型到数据库中

1. 在`settings.py`中，配置好`DATABASES`，做好数据库相关的配置。
2. 在`app`中的`models.py`中定义好模型，这个模型必须继承自`django.db.models`。
3. 将这个`app`添加到`settings.py`的`INSTALLED_APP`中。
4. 在命令行终端，进入到项目所在的路径，然后执行命令`python manage.py makemigrations`来生成迁移脚本文件。
5. 同样在命令行中，执行命令`python manage.py migrate`来将迁移脚本文件映射到数据库中。

### ORM中常用的Field

* 自定义的主见必须定义`primary_key=True`

##### BooleanField：

在模型层面接收的是`True/False`。在数据库层面是`tinyint`类型。如果没有指定默认值，默认值是`None`，如果想要使用可以为空的BooleanField，可以使用NullBooleanField。

##### DateField：

日期类型。在`Python`中是`datetime.date`类型，可以记录年月日。在映射到数据库中也是`date`类型。使用这个`Field`可以传递以下几个参数：

1. `auto_now`：在每次这个数据保存的时候，都使用当前的时间。比如作为一个记录修改日期的字段，可以将这个属性设置为`True`。
2. `auto_now_add`：在每次数据第一次被添加进去的时候，都使用当前的时间。比如作为一个记录第一次入库的字段，可以将这个属性设置为`True`。

### Navie time & Aware time

* Naive time 不知道自己的时间是哪个时区的
* Aware time 知道自己的时间是哪个时区的
* 因此，想要将一个时间转换成另外一个时区的时间，首先要保证这个时间是aware time
* pytz 专门处理时区的库，安装Django的时候会默认安装
* astimezone方法 讲一个时间转换为另外一个时区的时间，只能被awate time类型的时间调用
* replace 方法 可以更改一个时间的某些对象

~~~python

>>> import pytz
>>> from datetime import datetime
# 获取当前时间
>>> now = datetime.now()
>>> now
# 这是一个 navie time 类型的时间
datetime.datetime(2020, 2, 25, 6, 7, 13, 94871)

# 获取utc时区的时区对象
>>> utc_timezone = pytz.timezone('UTC')

# replace 方法 可以修改一个时间的某些属性
>>> now = now.replace(day=26) 
>>> now
datetime.datetime(2020, 2, 26, 6, 7, 13, 94871)

# 使用 replace方法将一个时间的时区设置为东八区亚洲上海
>>> now =now.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
>>> now
datetime.datetime(2020, 2, 26, 6, 7, 13, 94871, tzinfo=<DstTzInfo 'Asia/Shanghai' LMT+8:06:00 STD>)

# 使用astimezone 方法 将一个时间 转换成另一个时区的时间
>>> utc_now = now.astimezone(utc_timezone)
>>> utc_now
datetime.datetime(2020, 2, 25, 22, 1, 13, 94871, tzinfo=<UTC>)
~~~

### Navie time & Aware time 在Django中的使用

* 在Django中可以使用 `django.utils.timezone.now`方法 和 `django.utils.timezone.localtime `方法， `django.utils.timezone.now`会生成一个UTC的当前时间， `django.utils.timezone.localtime `会根据 `settings.py`中`TIME_ZONE`设置的时区生成一个相应的当前时间
* 在HTML模版中使用，可以`{% load tz %}` 使用 `{{ time|localtime }}` 将UTC时间转换为本地时间



### 模型中的Meta配置

我们可以在模型中定义一个类，叫做`Meta`。然后在这个类中添加一些类属性来控制模型的作用。比如我们想要在数据库映射的时候使用自己指定的表名，而不是使用模型的名称。那么我们可以在`Meta`类中添加一个`db_table`的属性。示例代码如下

* db_table

  这个模型映射到数据库中的表名。如果没有指定这个参数，那么在映射的时候将会使用模型名来作为默认的表名

* ordering

  设置在提取数据的排序方式，比如查找数据的时候根据添加的时间排序

```python
class Book(models.Model):
    name = models.CharField(max_length=20,null=False)
    desc = models.CharField(max_length=100,name='description',db_column="description1")
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'book_model'
        ordering = ['pub_date']
```



### 外键与表关系

在`MySQL`中，表有两种引擎，一种是`InnoDB`，另外一种是`myisam`。如果使用的是`InnoDB`引擎，是支持外键约束的。外键的存在使得`ORM`框架在处理表关系的时候异常的强大。因此这里我们首先来介绍下外键在`Django`中的使用。

类定义为`class ForeignKey(to,on_delete,**options)`。第一个参数是引用的是哪个模型，第二个参数是在使用外键引用的模型数据被删除了，这个字段该如何处理，比如有`CASCADE`、`SET_NULL`等。

~~~python
# ----------------- 外键与表关系 -----------------


class ORMCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return '<category:%s>' % self.name

    class Meta:
        db_table = 'orm_category'


class ORMArticle(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # on_delete=models.CASCADE 级联操作，如果外键对应的那条数据被删除了，那么这条数据也会被删除
    category = models.ForeignKey("ORMCategory", on_delete=models.CASCADE)

    # on_delete=models.PROTECT 受保护。即只要这条数据引用了外键的那条数据，那么就不能删除外键的那条数据。
    # category = models.ForeignKey("ORMCategory", on_delete=models.PROTECT)

    # on_delete=models.SET_NULL 设置为空。如果外键的那条数据被删除了，那么在本条数据上就将这个字段设置为空。如果设置这个选项，前提是要指定这个字段可以为空。
    # category = models.ForeignKey("ORMCategory", on_delete=models.SET_NULL, null=True)

    # on_delete=models.SET_DEFAULT 设置默认值。如果外键的那条数据被删除了，那么本条数据上就将这个字段设置为默认值。如果设置这个选项，前提是要指定这个字段一个默认值。
    # category = models.ForeignKey("ORMCategory", on_delete=models.SET_DEFAULT, default=ORMCategory.objects.get(pk=1))

    # on_delete=models.SET() SET()：如果外键的那条数据被删除了。那么将会获取SET函数中的值来作为这个外键的值。SET函数可以接收一个可以调用的对象（比如函数或者方法），如果是可以调用的对象，那么会将这个对象调用后的结果作为值返回回去。
    # category = models.ForeignKey("ORMCategory", on_delete=models.SET(ORMCategory.objects.get(pk=1)))
    # category = models.ForeignKey("ORMCategory", on_delete=models.SET(category_default))

    # 不采取任何行为。一切全看数据库级别的约束
    # category = models.ForeignKey("ORMCategory", on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<article:%s>' % self.title

    class Meta:
        db_table = 'orm_article'
        ordering = ['-created', 'id']  # 先按时间排序，如果时间相同按照id排序


# 自关联
class ORMComment(models.Model):
    content = models.TextField()
    origin_comment = models.ForeignKey('self', on_delete=models.CASCADE)

    def __str__(self):
        return '<comment:%s>' % self.id

    class Meta:
        db_table = 'orm_comment'


def category_default():
    return ORMCategory.objects.get(pk=1)

~~~

##### 关系表之一对多

一对多或者多对一，都是通过`ForeignKey`来实现的

* 在django当中，如果一个模型被另一个模型以外键的形式引用了，那么它就会自动的给这个模型添加一个属性，这个属性的名字就是   引用它的模型类的 类名称小写 加 下划线 ‘_’ 加 set（***__set），例如

  ~~~python
  class ORMCategory(models.Model):
      name = models.CharField(max_length=100)
  
  
  class ORMArticle(models.Model):
      title = models.CharField(max_length=100)
      content = models.TextField()
      category = models.ForeignKey("ORMCategory", on_delete=models.CASCADE)
      created = models.DateTimeField(auto_now_add=True)
  ~~~

  django就会自动的给 ORMCategory模型 添加一个属性 这个属性的名称叫做 `ormarticle_set`

* 如果不想使用 `ormarticle_set`的方式，可以在外键引用的地方添加`related_name`参数更改它的名字，例如：`related_name='articles'`

  ~~~python
  class ORMCategory(models.Model):
      name = models.CharField(max_length=100)
  
  
  class ORMArticle(models.Model):
      title = models.CharField(max_length=100)
      content = models.TextField()
      category = models.ForeignKey("ORMCategory", on_delete=models.CASCADE related_name='articles')
      created = models.DateTimeField(auto_now_add=True)
  ~~~


app3/views.py

~~~python
def orm2(request):
    ''' 一对多 反向查询 '''
    # 获取某个分类下所有的文章
    category = ORMCategory.objects.get(pk=9)
    articles = category.ormarticle_set.all()  # 获取所有的文章
    article = category.ormarticle_set.first()  # 获取第一篇文章
    print(articles)
    return HttpResponse()


def orm3(request):
    ''' 一对多 反向添加 1 '''
    category = ORMCategory.objects.first()

    # 如果要使用如下反向添加的方式，必须保证 外键设置了 null=True，不然 article.save() 就会报错
    article = ORMArticle(title='Python', content='This is Python String')
    article.save()  # 这里必须保证外键 添加了 null=True

    category.ormarticle_set.add(article)
    category.save()

    return HttpResponse()


def orm4(request):
    ''' 一对多 反向添加 2 '''

    category = ORMCategory.objects.first()

    # 如果 外键引用没有设置 null=True, 在反向添加的add方法中添加参数 bulk=False， bulk=False会自动遍历所有对象，并将他们保存
    article = ORMArticle(title='Python', content='This is Python String')

    category.ormarticle_set.add(article, bulk=False)

    return HttpResponse()

~~~

#####关系表之一对一

一对一是通过`OneToOneField`实现的，`OneToOneField`的本质其实就是一个外键，只不过这个外键有一个唯一约束 `unique key`

* 在django中，如果一个模型被另一个模型以一对一引用关联的话，那么它就会给这个模型添加一个属性，这个属性的名子就是 引用他的模型的 类名称的全部小写

  ~~~python
  class ORMFrontUser(models.Model):
      username = models.CharField(max_length=200)
  
  
  class UserExtension(models.Model):
      school = models.CharField(max_length=100)
      user = models.OneToOneField("ORMFrontUser", on_delete=models.CASCADE)
      
  ~~~

  django会自动给ORMFrontUser模型添加一个属性，这个属性的名称就是UserExtension模型类名称的全拼小写`userextension`

* 如果在使用过程(如 反向引用)中不想使用 引用模型的类名称的全部小写 那么可以设置`related_name`参数更改它的名子，如：`related_name='ext'`

  ~~~python
  class ORMFrontUser(models.Model):
      username = models.CharField(max_length=200)
      
  class UserExtension(models.Model):
      school = models.CharField(max_length=100)
      user = models.OneToOneField("ORMFrontUser", on_delete=models.CASCADE, related_name='ext')
  ~~~

app3/views.py

~~~python
def orm5(request):
    ''' 一对一 反向引用 '''

    # 如果模型 OneToOneField 没有设置 related_name，可以用一下方式反向引用
    front = ORMFrontUser.objects.first()
    ext = front.userextension

    # 如果模型 OneToOneField 设置了 related_name 那么必须使用 related_name 进行反向引用
    front = ORMFrontUser.objects.first()
    ext = front.ext  # 假设此时 OneToOneField 设置了 related_name='ext'

    print(ext)

    return HttpResponse()
~~~

##### 关系表之一对一

多对多是通过`ManyToManyField`来实现的，实际上`Django`是为这种多对多的关系建立了一个中间表。这个中间表分别定义了两个外键

* django会自动生成一个中间表，这个中间表定义了连接两个表的外键

* 在django中国，如果一个模型被另一个模型以多对多的形式引用关联，那么它就会给这个模型添加一个属性，这个属性的名字就是 引用它的模型的 类名称的全部小写 加 下划线`_` 加 set, 如：`ormtag_set`

  ~~~python
  class ORMTag(models.Model):
      name = models.CharField(max_length=100)
      articles = models.ManyToManyField("ORMArticle")
      
      
  class ORMArticle(models.Model):
      title = models.CharField(max_length=100)
      content = models.TextField()
      category = models.ForeignKey("ORMCategory", on_delete=models.CASCADE)
      created = models.DateTimeField(auto_now_add=True)
  ~~~

* 如果在使用过程中(如 反向引用)不想使用 引用模型的类名称 加下划线 加set 的方式，那么可以在`ManyToManyField`中设置`related_name`参数更改它的名字，如`related_name='exts'`

  ~~~python
  class ORMTag(models.Model):
      name = models.CharField(max_length=100)
  		articles = models.ManyToManyField("ORMArticle", related_name='tags')
  ~~~

app3/views.py

~~~python
def orm6(request):
    ''' 多对多 反向添加 '''

    article = ORMArticle.objects.first()
    tag = ORMTag(name='Language')
    tag.save()  # 再被反向添加之前必须save()，多对多关系(ManyToManyField)中的反向添加add方法没有 bulk 参数
    article.ormtag_set.add(tag)

    return HttpResponse(tag.name)


def orm7(request):
    ''' 多对多 正向添加 '''

    tag = ORMTag.objects.first()
    article = ORMArticle.objects.get(pk=10)
    tag.articles.add(article)

    return HttpResponse()
~~~

### ORM查询

* QuerySet.query 

  `query`可以查看`ORM`语句被翻译成的`SQL`语句，但是`query`中能作用在`QuerySet`对象上，因此只有`filter`等方法可以使用`query`，`get`方法则不能

* 如果要反向查询关联表的内容，直接通过 关联表名称的全部小写 加 双下划线`__`来连接，如`filterarticle__in`，并且不需要写 `models_set`的形式，这么做的前提是 被其它表引用的外键`ForeignKey`所在字段中没有添加参数`related_name`和`related_query_name`。

  如果设添加了`related_name`，没有添加`related_query_name`，那么就必须使用 `related_name`设定的值 加 双下划线 `__`, 。

  如果同时添加了`related_name`和`related_query_name`或者 只添加了`related_query_name`，那么就必须用 `related_query_name`设定的值 加 双下划线 `__`, 。

###### exact

精确查找，如果提过的是一个None，那么sql层面就被解释为null

app3/views.py

~~~python
def orm_filter1(request):
    ''' exact '''
    articles = FilterArticle.objects.filter(title__exact='Python')
    print(articles.query)
    print(articles)
    articles = FilterArticle.objects.filter(title__exact=None)
    print(articles.query)
    print(articles)
    return HttpResponse()
  
>>> SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content` FROM 		`filter_article` WHERE `filter_article`.`title` = Python
		<QuerySet [<FilterArticle: <article:Python>>]>
		SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content` FROM 		`filter_article` WHERE `filter_article`.`title` IS NULL
		<QuerySet []>
~~~



###### iexact

使用`like`进行查找

app3/views.py

~~~python
def orm_filter2(request):
    ''' iexact '''
    articles = FilterArticle.objects.filter(title__iexact='Python')
    print(articles.query)
    print(articles)
    return HttpResponse()
  
>>> SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content` FROM 		`filter_article` WHERE `filter_article`.`title` LIKE Python
		<QuerySet [<FilterArticle: <article:Python>>]>
~~~

* exact 和 iexact的区别就是 exact在底层会被翻译成`=`，iexact在底层会被翻译成`like`

###### contains

大小写敏感的查询匹配，判断某个字段是否包含了某个数据。翻译成`sql	`为`like binary`

app3/views.py

~~~python
def orm_filter3(request):
    ''' contains '''
    articles = FilterArticle.objects.filter(title__contains='PYTHON')
    print(articles.query)
    print(articles)
    return HttpResponse()

>>> SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content` FROM 		`filter_article` WHERE `filter_article`.`title` LIKE BINARY %PYTHON%
		<QuerySet []>
~~~

###### icontains

大小写不敏感的查询匹配

app3/views.py

~~~python
def orm_filter4(request):
    ''' icontains '''
    articles = FilterArticle.objects.filter(title__icontains='PYTHON')
    print(articles.query)
    print(articles)
    return HttpResponse()

>>> SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content` FROM 	  `filter_article` WHERE `filter_article`.`title` LIKE %PYTHON%
	  <QuerySet [<FilterArticle: <article:Python>>]>
~~~

###### in

提取那些给定的`field`的值是否在给定的容器中。容器可以为`list`、`tuple`或者任何一个可以迭代的对象，包括`QuerySet`对象。翻译成`sql	`为`in`

app3/views.py

~~~python
def orm_filter5(request):
    ''' in '''
    articles = FilterArticle.objects.filter(id__in=[1, 2, 3])
    print(articles.query)
    print(articles)
    articles = FilterArticle.objects.filter(id__in=(1, 2, 3))
    print(articles.query)
    print(articles)
    articles = FilterArticle.objects.filter(id__in=FilterArticle.objects.filter(content__icontains='this is'))
    print(articles.query)
    print(articles)
    
    categories = FilterCategory.objects.filter(filterarticle__in=[1, 2, 3])
    print(categories.query)
    print(categories)
    return HttpResponse()

>>> SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content` FROM 		`filter_article` WHERE `filter_article`.`id` IN (1, 2, 3)
		<QuerySet [<FilterArticle: <article:Python>>, <FilterArticle: <article:Django>>, 				<FilterArticle: <article:Flask>>]>
  
		SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content` FROM 		`filter_article` WHERE `filter_article`.`id` IN (1, 2, 3)
		<QuerySet [<FilterArticle: <article:Python>>, <FilterArticle: <article:Django>>, 	<FilterArticle: <article:Flask>>]>
    
		SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content` FROM 		`filter_article` WHERE `filter_article`.`id` IN (SELECT U0.`id` FROM `filter_article` U0 		 WHERE U0.`content` LIKE %this is%)
		<QuerySet [<FilterArticle: <article:Python>>, <FilterArticle: <article:Django>>, 	<FilterArticle: <article:Flask>>]>
    SELECT `filter_category`.`id`, `filter_category`.`name` FROM `filter_category` INNER 				JOIN `filter_article` ON (`filter_category`.`id` = `filter_article`.`category_id`) WHERE 		`filter_article`.`id` IN (1, 2, 3)
		<QuerySet [<FilterCategory: Python>, <FilterCategory: Python>, <FilterCategory: Python>]>
~~~

###### gt、gte、lt、lte

大于、大于等于、小于、小于等于

~~~python


>>> SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content`, 				`filter_article`.`category_id` FROM `filter_article` WHERE `filter_article`.`id` > 2
		<QuerySet [<FilterArticle: <article:Flask>>]>
  
		SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content`, 		`filter_article`.`category_id` FROM `filter_article` WHERE `filter_article`.`id` >= 2
    <QuerySet [<FilterArticle: <article:Django>>, <FilterArticle: <article:Flask>>]>
    
		SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content`, `filter_article`.`category_id` FROM `filter_article` WHERE `filter_article`.`id` < 2
		<QuerySet [<FilterArticle: <article:Python>>]>
    
		SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content`, `filter_article`.`category_id` FROM `filter_article` WHERE `filter_article`.`id` <= 2
		<QuerySet [<FilterArticle: <article:Python>>, <FilterArticle: <article:Django>>]>
~~~

###### startswith、istartswith、endswith、iendswith

以某个值开头或者结尾、大小写敏感或者不敏感

app3/views.py

~~~python
def orm_filter7(request):
    ''' startswith、istartswith、endswith、iendswith '''

    # 大小写敏感
    articles = FilterArticle.objects.filter(title__startswith='python')
    print(articles.query)
    print(articles)
    articles = FilterArticle.objects.filter(title__endswith='python')
    print(articles.query)
    print(articles)

    # 大小写不敏感
    articles = FilterArticle.objects.filter(title__startswith='python')
    print(articles.query)
    print(articles)
    articles = FilterArticle.objects.filter(title__endswith='python')
    print(articles.query)
    print(articles)
    return HttpResponse()
  
SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content`, `filter_article`.`category_id` FROM `filter_article` WHERE `filter_article`.`title` LIKE BINARY python%
<QuerySet []>
SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content`, `filter_article`.`category_id` FROM `filter_article` WHERE `filter_article`.`title` LIKE BINARY %python
<QuerySet []>
SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content`, `filter_article`.`category_id` FROM `filter_article` WHERE `filter_article`.`title` LIKE BINARY python%
<QuerySet []>
SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content`, `filter_article`.`category_id` FROM `filter_article` WHERE `filter_article`.`title` LIKE BINARY %python
<QuerySet []>
~~~

###### range

判断某个`field`的值是否在给定的区间中

app3/views.py

~~~python
def orm_filter8(request):
    ''' rang '''
    # make_aware 创建一个 aware time
    start_time = make_aware(datetime(year=2020, month=2, day=26, hour=12, minute=0, second=0))
    end_time = make_aware(datetime(year=2020, month=2, day=27, hour=12, minute=0, second=0))
    articles = FilterArticle.objects.filter(created__range=(start_time, end_time))
    print(articles.query)
    print(articles)
    return HttpResponse()

 SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content`, `filter_article`.`category_id`, `filter_article`.`created` FROM `filter_article` WHERE `filter_article`.`created` BETWEEN 2020-02-26 04:00:00 AND 2020-02-27 04:00:00
<QuerySet [<FilterArticle: <article:Python>>, <FilterArticle: <article:Django>>, <FilterArticle: <article:Flask>>]>
~~~

###### date、year、month、day、weekday、time

* 针对某些`date`或者`datetime`类型的字段。可以指定`date`的范围。并且这个时间过滤，还可以使用链式调用

~~~python
def orm_filter9(request):
    articles = FilterArticle.objects.filter(created__date=datetime(year=2020, month=2, day=26))
    print(articles.query)
    print(articles)
    return HttpResponse()

SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content`, `filter_article`.`category_id`, `filter_article`.`created` FROM `filter_article` WHERE DATE(CONVERT_TZ(`filter_article`.`created`, 'UTC', 'Asia/Shanghai')) = 2020-02-26
<QuerySet []>
~~~

* year、month、day
* weekday
  * 同`year`，根据星期几进行查找。1表示星期天，7表示星期六，`2-6`代表的是星期一到星期五。

~~~python
def orm_filter9(request):
    ''' date '''
    articles = FilterArticle.objects.filter(created__date=datetime(year=2020, month=2, day=26))
    print(articles.query)
    print(articles)

    ''' year、month、day、weekday '''
    articles = FilterArticle.objects.filter(created__year__gte=2019)
    print(articles.query)
    print(articles)

    articles = FilterArticle.objects.filter(created__month=2)
    print(articles.query)
    print(articles)

    articles = FilterArticle.objects.filter(created__day__lte=27)
    print(articles.query)
    print(articles)

    articles = FilterArticle.objects.filter(created__week_day=3)
    print(articles.query)
    print(articles)

    return HttpResponse()
  
SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content`, `filter_article`.`category_id`, `filter_article`.`created` FROM `filter_article` WHERE DATE(CONVERT_TZ(`filter_article`.`created`, 'UTC', 'Asia/Shanghai')) = 2020-02-26
<QuerySet []>
SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content`, `filter_article`.`category_id`, `filter_article`.`created` FROM `filter_article` WHERE `filter_article`.`created` >= 2018-12-31 16:00:00
<QuerySet [<FilterArticle: <article:Python>>, <FilterArticle: <article:Django>>, <FilterArticle: <article:Flask>>]>
SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content`, `filter_article`.`category_id`, `filter_article`.`created` FROM `filter_article` WHERE EXTRACT(MONTH FROM CONVERT_TZ(`filter_article`.`created`, 'UTC', 'Asia/Shanghai')) = 2
<QuerySet []>
SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content`, `filter_article`.`category_id`, `filter_article`.`created` FROM `filter_article` WHERE EXTRACT(DAY FROM CONVERT_TZ(`filter_article`.`created`, 'UTC', 'Asia/Shanghai')) <= 27
<QuerySet []>
SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content`, `filter_article`.`category_id`, `filter_article`.`created` FROM `filter_article` WHERE DAYOFWEEK(CONVERT_TZ(`filter_article`.`created`, 'UTC', 'Asia/Shanghai')) = 3
<QuerySet []>
~~~

###### isunll

根据值是否为空

~~~python
def orm_filter10(request):
    ''' isnull '''

    articles = FilterArticle.objects.filter(title__isnull=True)
    print(articles.query)
    print(articles)

    return HttpResponse()

SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content`, `filter_article`.`category_id`, `filter_article`.`created` FROM `filter_article` WHERE `filter_article`.`title` IS NULL
<QuerySet []>
~~~

###### regex & iregex

大小写敏感和大小写不敏感的正则表达式。

~~~python
def orm_filter11(request):
    ''' regex & iregex '''

    articles = FilterArticle.objects.filter(title__regex='Python')
    print(articles.query)
    print(articles)

    articles = FilterArticle.objects.filter(title__iregex='Python')
    print(articles.query)
    print(articles)

    return HttpResponse()

SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content`, `filter_article`.`category_id`, `filter_article`.`created` FROM `filter_article` WHERE REGEXP_LIKE(`filter_article`.`title`, Python, 'c')
<QuerySet [<FilterArticle: <article:Python>>]>
SELECT `filter_article`.`id`, `filter_article`.`title`, `filter_article`.`content`, `filter_article`.`category_id`, `filter_article`.`created` FROM `filter_article` WHERE REGEXP_LIKE(`filter_article`.`title`, Python, 'i')
<QuerySet [<FilterArticle: <article:Python>>]>
~~~

### 反向引用 & 反向查询

* 反向引用是将 引用了自己的模型的名称 全部小写 加 下划线`_` 加 `set`，可以通过添加`related_name`来更改它的使用名称
* 反向查询是将 引用了自己的模型的名称 全部小写 加 双下划线 `__` ，可以通过添加`related_query_name`来更改它的使用名称

#### related_name：

还是以`User`和`Article`为例来进行说明。如果一个`article`想要访问对应的作者，那么可以通过`author`来进行访问。但是如果有一个`user`对象，想要通过这个`user`对象获取所有的文章，该如何做呢？这时候可以通过`user.article_set`来访问，这个名字的规律是`模型名字小写_set`。示例代码如下：

```python
user = User.objects.get(name='张三')
user.article_set.all()
```

如果不想使用`模型名字小写_set`的方式，想要使用其他的名字，那么可以在定义模型的时候指定`related_name`。示例代码如下：

```python
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # 传递related_name参数，以后在方向引用的时候使用articles进行访问
    author = models.ForeignKey("User",on_delete=models.SET_NULL,null=True,related_name='articles')
```

以后在方向引用的时候。使用`articles`可以访问到这个作者的文章模型。示例代码如下：

```python
user = User.objects.get(name='张三')
user.articles.all()
```

如果不想使用反向引用，那么可以指定`related_name='+'`。示例代码如下：

```python
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # 传递related_name参数，以后在方向引用的时候使用articles进行访问
    author = models.ForeignKey("User",on_delete=models.SET_NULL,null=True,related_name='+')
```

以后将不能通过`user.article_set`来访问文章模型了。

#### related_query_name：

在查找数据的时候，可以使用`filter`进行过滤。使用`filter`过滤的时候，不仅仅可以指定本模型上的某个属性要满足什么条件，还可以指定相关联的模型满足什么属性。比如现在想要获取写过标题为`abc`的所有用户，那么可以这样写：

```python
users = User.objects.filter(article__title='abc')
```

如果你设置了`related_name`为`articles`，因为反转的过滤器的名字将使用`related_name`的名字，那么上例代码将改成如下：

```python
users = User.objects.filter(articles__title='abc')
```

可以通过`related_query_name`将查询的反转名字修改成其他的名字。比如`article`。示例代码如下：

```python
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # 传递related_name参数，以后在方向引用的时候使用articles进行访问
    author = models.ForeignKey("User",on_delete=models.SET_NULL,null=True,related_name='articles',related_query_name='article')
```

那么在做反向过滤查找的时候就可以使用以下代码：

```python
users = User.objects.filter(article__title='abc')
```

### 聚合函数

* 所有的聚合函数都放在`django.dv.models`下面
* 聚合函数不能够单独执行，需要放到可以执行聚合函数的方法中去执行，如`aggregate`和`annotate`
* 聚合函数执行完成，会默认给它的结果一个变量名，这个名称由 字段名+`__`+聚合函数名称小写拼接而成，如：`price__avg`，当然也可以自定义这个变量名，如：`avg=Avg('price')`

##### aggregate和annotate的区别：

1. `aggregate`：返回使用聚合函数后的字段和值。
   * aggregat：针对所有对象
   * aggregate 返回一个字典，字典内容为聚合函数执行的结果。
2. `annotate`：在原来模型字段的基础之上添加一个使用了聚合函数的字段，并且在使用聚合函数的时候，会使用当前这个模型的主键进行分组（group by）
   * annotate：针对单独的每一个对象
   * annotate返回一个QuerySet对象，并且会在查找的模型上添加一个聚合函数执行结果的属性
   * annotate会使用`group by`根据查找对象的主键分组

~~~python
def orm_filter12(request):
    ''' Avg '''

    # 求图书定价的平均值
    result = FilterBook.objects.aggregate(Avg('price'))
    print(result)
    print(connection.queries)  # 使用 connection.queries 查看 sql 语句

    # aggregate 返回一个字典，字典内容为聚合函数执行的结果
    # django 默认 aggregate返回的字典的key为 字段名 加 双下划线 加 聚合函数的名称小写
    # 这个key可以自定义，如：
    result = FilterBook.objects.aggregate(avg=Avg('price'))
    print(result)
    print(connection.queries)

    # 获取每一本书售价的平均值
    result = FilterBook.objects.annotate(
        avg=Avg('filterbookorder__price'))  # 这里使用到的是反向查询，ForeignKey 中没有添加related_name 和 related_query_name
    for r in result:
        print(r.name, r.avg)
    print(connection.queries)

    return HttpResponse('Avg')


def orm_filter13(request):
    ''' Count '''

    # 求图书的总量
    result = FilterBook.objects.aggregate(count=Count('id'))
    print(result)

    # 求每一本书的销售总量
    result = FilterBook.objects.annotate(count=Count('filterbookorder__id'))
    for r in result:
        print(r.name, r.count)

    return HttpResponse('Count')


def orm_filter14(request):
    ''' Max & Min '''

    # 求所有图书的最大销售额和最小销售额
    p_max = FilterBook.objects.aggregate(p_max=Max('filterbookorder__price'))
    print(p_max)
    p_min = FilterBook.objects.aggregate(p_min=Min('filterbookorder__price'))
    print(p_min)

    # 求每一本图书的最大销售额和最小销售额
    result = FilterBook.objects.annotate(p_max=Max('filterbookorder__price'))
    for r in result:
        print(r.name, r.p_max)

    result = FilterBook.objects.annotate(p_min=Min('filterbookorder__price'))
    for r in result:
        print(r.name, r.p_min)

    return HttpResponse('Max & Min')


def orm_filter15(request):
    ''' Sum '''

    # 求说有图书的总销售额
    result = FilterBook.objects.aggregate(sum=Sum('filterbookorder__price'))
    print(result)

    # 求每一本书的销售总额
    result = FilterBook.objects.annotate(sum=Sum('filterbookorder__price'))
    for r in result:
        print(r.name, r.sum)

    return HttpResponse('Sum')
~~~

### F表达式

`F表达式`是用来优化`ORM`操作数据库的。比如我们要将公司所有员工的薪水都增加1000元，如果按照正常的流程，应该是先从数据库中提取所有的员工工资到Python内存中，然后使用Python代码在员工工资的基础之上增加1000元，最后再保存到数据库中。这里面涉及的流程就是，首先从数据库中提取数据到Python内存中，然后在Python内存中做完运算，之后再保存到数据库中。示例代码如下：

```python
employees = Employee.objects.all()
for employee in employees:
    employee.salary += 1000
    employee.save()
```

而我们的`F表达式`就可以优化这个流程，他可以不需要先把数据从数据库中提取出来，计算完成后再保存回去，他可以直接执行`SQL语句`，就将员工的工资增加1000元。示例代码如下：

```python
from djang.db.models import F
Employee.object.update(salary=F("salary")+1000)
```

`F表达式`并不会马上从数据库中获取数据，而是在生成`SQL`语句的时候，动态的获取传给`F表达式`的值。

比如如果想要获取作者中，`name`和`email`相同的作者数据。如果不使用`F表达式`，那么需要使用以下代码来完成：

```python
    authors = Author.objects.all()
    for author in authors:
        if author.name == author.email:
            print(author)
```

如果使用`F表达式`，那么一行代码就可以搞定。示例代码如下：

```python
    from django.db.models import F
    authors = Author.objects.filter(name=F("email"))
```

* 动态的获取某个字段上的值，不会真正去数据库查询数据，它相当于一个标识作用

~~~python
def orm_filter16(request):
    ''' F 表达式 '''

    # 给多有书籍的价格增加10
    FilterBook.objects.update(price=F('price') + 10)

    # 查重价格和销售价格相同的书籍
    result = FilterBook.objects.filter(price=F('filterbookorder__price'))
    for r in result:
        print(r.name)

    return HttpResponse('F 表达式 ')
~~~



### Q表达式

如果想要实现所有价格高于100元，并且评分达到9.0以上评分的图书。那么可以通过以下代码来实现：

```python
books = Book.objects.filter(price__gte=100,rating__gte=9)
```

以上这个案例是一个并集查询，可以简单的通过传递多个条件进去来实现。
但是如果想要实现一些复杂的查询语句，比如要查询所有价格低于10元，`或者` 是评分低于9分的图书。那就没有办法通过传递多个条件进去实现了。这时候就需要使用`Q表达式`来实现了。示例代码如下：

```python
from django.db.models import Q
books = Book.objects.filter(Q(price__lte=10) | Q(rating__lte=9))
```

以上是进行或运算，当然还可以进行其他的运算，比如有`&`和`~（非）`等。一些用`Q`表达式的例子如下：

```python
from django.db.models import Q
# 获取id等于3的图书
books = Book.objects.filter(Q(id=3))
# 获取id等于3，或者名字中包含文字"记"的图书
books = Book.objects.filter(Q(id=3)|Q(name__contains("记")))
# 获取价格大于100，并且书名中包含"记"的图书
books = Book.objects.filter(Q(price__gte=100)&Q(name__contains("记")))
# 获取书名包含“记”，但是id不等于3的图书
books = Book.objects.filter(Q(name__contains='记') & ~Q(id=3))
```

* 支持与或非操作

~~~python
def orm_filter17(request):
    ''' Q 表达式 '''
    # 或操作
    # 获取评分大于9.8 或者 价格大于100 的书籍
    # 或者、或者、或者 重要的事情说三遍

    result = FilterBook.objects.filter(Q(rating__gt=9.8) | Q(price__gte=100))
    for r in result:
        print(r.name)
    # 与操作
    # 获取评分大于9.8 并且 价格大于100 的书籍
    # 并且、并且、并且 重要的事情说三遍

    result = FilterBook.objects.filter(Q(rating__gt=9.8) & Q(price__gte=100))
    for r in result:
        print(r)

    # 非操作
    # 获取价格大于100 并且图书名称不包含'j'的书籍
    # 不包含'j'、不包含'j'、不包含'j'
    result = FilterBook.objects.filter(Q(price__gte=100) & ~Q(name__contains='j'))
    for r in result:
        print(r.name)
    return HttpResponse('Q 表达式')
~~~

### object对象所属类原理分析

~~~python
def orm_filter18(request):
    ''' object对象所属类原理分析 '''

    # 查看objects到底代表的是什么对象
    print(type(FilterBook.objects))  # 使用type查看FilterBook是属于哪个类
    # 返回结果为 <class 'django.db.models.manager.Manager'>
    # 因此 FilterBook 是属于 Manager 类的

    # 查看 Manager 类
    # from django.db.models.manager import Manager

    '''
    Manager:
    
    class Manager(BaseManager.from_queryset(QuerySet)):
    pass
    
    1.Manage 的父类 BaseManager.from_queryset(QuerySet) 是动态生成的，
    2.是由 BaseManager 调用类方法 from_queryset 方法
    3.from_queryset 传递了一个参数 QuerySet
    4.这里的 QuerySet 是一个类
    
    '''

    # 查看 from_queryset 方法
    '''
    from_queryset 方法:
    
    @classmethod
    def from_queryset(cls, queryset_class, class_name=None):
        if class_name is None:
            class_name = '%sFrom%s' % (cls.__name__, queryset_class.__name__)
        return type(class_name, (cls,), {
            '_queryset_class': queryset_class,
            **cls._get_queryset_methods(queryset_class),
        })
        
    1.此时的 cls 是 BaseManager，因此 cls.__name__='BaseManager'
    
    2.此时的 queryset_class 是 QuerySet，因此 class_name = 'BaseManagerFromQuerySet'
    
    3.'_queryset_class': queryset_class, ==> '_queryset_class':QuerySet
    
    4.cls._get_queryset_methods(queryset_class) ==> cls._get_queryset_methods(QuerySet)
    
    5.使用 _get_queryset_methods()方法 收集 QuerySet类 的方法和属性
    
    6.使用 type(class_name, (cls,), {...}) 动态的创建一个类:
    type(BaseManagerFromQuerySet, (BaseManager,), {'_queryset_class':QuerySet, cls._get_queryset_methods(QuerySet)})
    
    7.返回type()方法创建的类
    
    '''

    '''
    type方法动态创建一个类
    type(class_name, (cls,), {...})
    第一个参数为 创建的类的类名名称
    第二个参数为 要创建的类的父亲类
    第三个参数为 要创建的类的属性和方法
    '''

    # 查看 _get_queryset_methods()方法
    '''
    _get_queryset_methods()方法:
    
    @classmethod
    def _get_queryset_methods(cls, queryset_class):
        def create_method(name, method):
            def manager_method(self, *args, **kwargs):
                return getattr(self.get_queryset(), name)(*args, **kwargs)
            manager_method.__name__ = method.__name__
            manager_method.__doc__ = method.__doc__
            return manager_method

        new_methods = {}
        for name, method in inspect.getmembers(queryset_class, predicate=inspect.isfunction):
            # Only copy missing methods.
            if hasattr(cls, name):
                continue
            # Only copy public methods or methods with the attribute `queryset_only=False`.
            queryset_only = getattr(method, 'queryset_only', None)
            if queryset_only or (queryset_only is None and name.startswith('_')):
                continue
            # Copy the method onto the manager.
            new_methods[name] = create_method(name, method)
        return new_methods
        
        
        1.此时的 queryset_class 是 QuerySet
        
        2.inspect.getmembers(queryset_class, predicate=inspect.isfunction)获取所有成员(属性和方法):
        predicate=inspect.isfunction 表示只获取函数方法
        ==> inspect.getmembers(QuerySet, predicate=inspect.isfunction) 获取 QuerySet 的所有方法
        
        3.将 QuerySet 中的方法 放到 new_methods
        
        因此，这里 _get_queryset_methods()方法 是将 QuerySet的所有方法拷贝出来
    '''

    # 总结：objects 拥有 QuerySet 的所有方法

    return HttpResponse('objects')
~~~

### QuerySet API 详解

* 可以进行链式调用，即`filter().filter()`的方式

###### exclude

排除满足条件的数据，返回一个新的`QuerySet`

~~~python
def queryset1(request):
    ''' exclude '''

    # 获取评分不小于9.8的书籍
    # 用Q表达式
    result = FilterBook.objects.filter(~Q(rating__lt=9.8))
    for book in result:
        print(book.name)

    # 使用 exclude 方法
    result = FilterBook.objects.exclude(rating__lt=9.8)
    for book in result:
        print(book.name)

    return HttpResponse('QuerySet API -- exclude')
~~~

###### order_by

指定将查询的结果根据某个字段进行排序。如果要倒叙排序，那么可以在这个字段的前面加一个负号。

~~~python
def queryset2(request):
    ''' order_by '''

    # 通过价格排序
    result = FilterBook.objects.order_by('price')
    print(result)

    # 通过价格倒叙排序
    result = FilterBook.objects.order_by('-price')
    print(result)

		# 先通过价格倒叙排序，如果价格相同，再通过页数排序
    result = FilterBook.objects.order_by('-price', 'page')
    print(result)

    return HttpResponse('QuerySet API -- order_by')
  
  	# 如果使用order_by().order_by, 后面的order_by将覆盖前面的order_by
    result = FilterBook.objects.order_by('-price').order_by('page')  # 最终会根据 page排序
~~~

###### annotate

给`QuerySet`中的每个对象都添加一个使用查询表达式（聚合函数、F表达式、Q表达式、Func表达式等）的新字段。

~~~python
def queryset3(request):
    ''' annotate '''

    # 给每一本书籍添加一个作者名
    result = FilterBook.objects.annotate(author_name=F('author__name'))
    # 通过这样的方式一次就可以查询出来，而如果使用book.author.name需要再进行一次查询
    for book in result:
        print(book.author_name)

    return HttpResponse('QuerySet API -- annotate')
~~~

###### values

用来指定提取需要的字段，默认情况下会把表中所有的字段全部都提取出来，可以使用`values`来进行指定，并且使用了`values`方法后，提取出的`QuerySet`中的数据类型不是模型，而是在`values`方法中指定的字段和值形成的字典。

~~~python
def queryset4(request):
    ''' values '''

    result = FilterBook.objects.values('name', 'price')
    for book in result:
        print(book)

    result = FilterBook.objects.values('name', author_name=F('author__name'), publisher_name=F('publisher__name'))
    for book in result:
        print(book)

    return HttpResponse('QuerySet API -- values')
  
{'name': 'python', 'price': 90.0}
{'name': 'django', 'price': 100.0}
{'name': 'flask', 'price': 80.0}
{'name': 'linux', 'price': 88.0}
{'name': 'javascript', 'price': 100.0}
{'name': 'react', 'price': 188.0}
{'name': 'python', 'author_name': 'ku_rong', 'publisher_name': 'qinghua'}
{'name': 'django', 'author_name': 'chen', 'publisher_name': 'qinghua'}
{'name': 'flask', 'author_name': 'rong', 'publisher_name': 'qinghua'}
{'name': 'linux', 'author_name': 'ronggege', 'publisher_name': 'bieda'}
{'name': 'javascript', 'author_name': 'chen', 'publisher_name': 'bieda'}
{'name': 'react', 'author_name': 'rong', 'publisher_name': 'bieda'}
~~~

###### values_list

类似于`values`。只不过返回的`QuerySet`中，存储的不是字典，而是元组。如果在`values_list`中只有一个字段。那么你可以传递`flat=True`来将结果扁平化。

~~~python
def queryset5(request):
    ''' values_list '''

    result = FilterBook.objects.values_list('name', 'page')
    print(result)

    result = FilterBook.objects.values_list('name')
    print(result)

    result = FilterBook.objects.values_list('name', flat=True)
    print(result)

    return HttpResponse('QuerySet API -- values_list')

<QuerySet [('python', 100), ('django', 110), ('flask', 120), ('linux', 130), ('javascript', 140), ('react', 150)]>
<QuerySet [('python',), ('django',), ('flask',), ('linux',), ('javascript',), ('react',)]>
<QuerySet ['python', 'django', 'flask', 'linux', 'javascript', 'react']>
~~~

###### select_related

在提取某个模型的数据的同时，也提前将相关联的数据提取出来。比如提取文章数据，可以使用`select_related`将`author`信息提取出来，以后再次使用`article.author`的时候就不需要再次去访问数据库了。可以减少数据库查询的次数。示例

~~~python
def queryset6(request):
    ''' select_related '''

    result = FilterBook.objects.select_related('author', 'publisher')
    for book in result:
        print(book.author, book.publisher)

    return HttpResponse('QuerySet API -- select_related')
~~~

⚠️`select_related`只能用在`一对多`或者`一对一`中，不能用在`多对多`或者`多对一`中。比如可以提前获取文章的作者，但是不能通过作者获取这个作者的文章，或者是通过某篇文章获取这个文章所有的标签。

###### prefetch_related

这个方法和`select_related`非常的类似，就是在访问多个表中的数据的时候，减少查询的次数。这个方法是为了解决`多对一`和`多对多`的关系的查询问题。

它只会产生连个sql查询

~~~python
def queryset7(request):
    ''' prefetch_related '''

    result = FilterBook.objects.prefetch_related('filterbookorder_set')
    for book in result:
        bookorders = book.filterbookorder_set.all()
        print(book.name)
        for order in bookorders:
            print(order.price)

    return HttpResponse('QuerySet API -- prefetch_related')
~~~

但是如果在使用`article.tag_set`的时候，如果又创建了一个新的`QuerySet`那么会把之前的`SQL`优化给破坏掉。比如以下代码：

~~~python
def queryset7(request):
    ''' prefetch_related '''

    result = FilterBook.objects.prefetch_related('filterbookorder_set')
    for book in result:
        bookorders = book.filterbookorder_set.filter(price__gte=90)
        print(book.name)
        for order in bookorders:
            print(order.price)

    return HttpResponse('QuerySet API -- prefetch_related')
~~~

那如果确实是想要在查询的时候指定过滤条件该如何做呢，这时候我们可以使用`django.db.models.Prefetch`来实现，`Prefetch`这个可以提前定义好`queryset`。示例代码如下：

~~~python 
def queryset7(request):
    ''' prefetch_related '''

    prefetch = Prefetch('filterbookorder_set', queryset=FilterBookOrder.objects.filter(price__gte=90))
    result = FilterBook.objects.prefetch_related(prefetch)
    for book in result:
        print(book.name)
        orders = book.filterbookorder_set.all()
        for order in orders:
            print(order.price)

    return HttpResponse('QuerySet API -- prefetch_related')
~~~

###### defer & only

* Defer

`defer`：在一些表中，可能存在很多的字段，但是一些字段的数据量可能是比较庞大的，而此时你又不需要，比如我们在获取文章列表的时候，文章的内容我们是不需要的，因此这时候我们就可以使用`defer`来过滤掉一些字段。这个字段跟`values`有点类似，只不过`defer`返回的不是字典，而是模型。

⚠️：如果在查询结果上获取了过滤掉的字段，那么就会继续增加查询

* Only

`defer`虽然能过滤字段，但是有些字段是不能过滤的，比如`id`，即使你过滤了，也会提取出来。

~~~python
def queryset8(request):
    ''' defer & only '''

    # defer
    result = FilterBook.objects.defer('page')  # 将page过滤调

    for book in result:
        print(book.page)  # 如果再获取了已经过滤掉的字段，那么它就会去重新查询

    # only
    result = FilterBook.objects.only('page')  # 只获取page

    return HttpResponse('QuerySet API -- defer & only')
~~~

###### get_or_create & bulk_creat

* get_or_create

根据某个条件进行查找，如果找到了那么就返回这条数据，如果没有查找到，那么就创建一个

注意⚠️：`get_or_create`返回一个元组，其中两个变量，一个是找到或者创建的对象，另一个是这个对象是否由创建而来，如果是创建的就返回`Ture`，找到的就返回`False`

* bulk_create

一次性创建多个数据。

~~~python
def queryset9(request):
    ''' get_or_create & bulk_create '''

    # get_or_create
    resutl = FilterPublish.objects.get_or_create(name='kurong')  # 数据库中有
    print(resutl)  # 结果：(< FilterPublish: kurong >, True)
    resutl = FilterPublish.objects.get_or_create(name='qinghua')  # 数据库中没有
    print(resutl)  # 结果：(< FilterPublish: qinghua >, False)

    # bulk_create
    resutl = FilterPublish.objects.bulk_create([
        FilterPublish(name='chenrong'),
        FilterPublish(name='ronggege'),
        FilterPublish(name='rong_ku')
    ])

    print(resutl)  # 结果：[<FilterPublish: chenrong>, <FilterPublish: ronggege>, <FilterPublish: rong_ku>]

    return HttpResponse('QuerySet API -- get_or_create & bulk_create')
~~~

###### count、exists、distinct、update、delete、切片操作

* count

  获取提取的数据的个数。如果想要知道总共有多少条数据，那么建议使用`count`，而不是使用`len(articles)`这种。因为`count`在底层是使用`select count(*)`来实现的，这种方式比使用`len`函数更加的高效。

* exists

  判断某个条件的数据是否存在。如果要判断某个条件的元素是否存在，那么建议使用`exists`，这比使用`count`或者直接判断`QuerySet`更有效得多。

* distinct

  去除掉那些重复的数据。这个方法如果底层数据库用的是`MySQL`，那么不能传递任何的参数。比如想要提取所有销售的价格超过80元的图书，并且删掉那些重复的，那么可以使用`distinct`来帮我们实现

  注意⚠️：`distinct`和`order_by`一起使用的话也会吧`order_by`中的字段考虑到唯一性里面

* update

  执行更新操作，在`SQL`底层走的也是`update`命令。

  注意⚠️：`update`不能和`get`一起使用

* delete

  删除所有满足条件的数据。删除数据的时候，要注意`on_delete`指定的处理方式。

* 切片操作

  有时候我们查找数据，有可能只需要其中的一部分。那么这时候可以使用切片操作来帮我们完成。`QuerySet`使用切片操作就跟列表使用切片操作是一样的。

~~~python
def queryset10(request):
    ''' count、exists、distinct、update、delete、切片操作 '''

    # count
    result = FilterBook.objects.filter(filterbookorder__price__gt=90).count()
    print(result)  # 7

    # exists
    result = FilterBook.objects.filter(author__name='Kurong').exists()
    print(result)  # False

    # exists 效率比 count 高
    if FilterBook.objects.filter(author__name='Kurong').count() > 0:
        print(result)

    # exists 效率比 QuerySet 高
    if FilterBook.objects.filter(author__name='Kurong'):
        print(result)

    # distinct
    result = FilterBook.objects.filter(filterbookorder__price__gt=90).distinct()
    print(result)
    # <QuerySet [<FilterBook: python>, <FilterBook: linux>, <FilterBook: react>, <FilterBook: flask>, <FilterBook: javascript>]>

    # update
    result = FilterBook.objects.update(price=F('price') + 5)
    print(result)
    result = FilterPublish.objects.filter(pk=3).update(name='ku_rong')
    print(result)

    # delete
    # FilterPublish.objects.get(pk=1).delete()

    # 切片操作
    result = FilterPublish.objects.all()[:3]
    print(result)
    result = FilterPublish.objects.get_queryset()[:3]
    print(result)

    return HttpResponse('QuerySet API -- count、exists、distinct、update、delete、切片操作')
~~~

### 什么时候`Django`会将`QuerySet`转换为`SQL`去执行：

生成一个`QuerySet`对象并不会马上转换为`SQL`语句去执行。
比如我们获取`Book`表下所有的图书：

```python
books = Book.objects.all()
print(connection.queries)
```

我们可以看到在打印`connection.quries`的时候打印的是一个空的列表。说明上面的`QuerySet`并没有真正的执行。
在以下情况下`QuerySet`会被转换为`SQL`语句执行：

1. 迭代：在遍历`QuerySet`对象的时候，会首先先执行这个`SQL`语句，然后再把这个结果返回进行迭代。比如以下代码就会转换为`SQL`语句：

   ```python
    for book in Book.objects.all():
        print(book)
   ```

2. 使用步长做切片操作：`QuerySet`可以类似于列表一样做切片操作。做切片操作本身不会执行`SQL`语句，但是如果如果在做切片操作的时候提供了步长，那么就会立马执行`SQL`语句。需要注意的是，做切片后不能再执行`filter`方法，否则会报错。

3. 调用`len`函数：调用`len`函数用来获取`QuerySet`中总共有多少条数据也会执行`SQL`语句。

4. 调用`list`函数：调用`list`函数用来将一个`QuerySet`对象转换为`list`对象也会立马执行`SQL`语句。

5. 判断：如果对某个`QuerySet`进行判断，也会立马执行`SQL`语句。

[
](../di-wu-zhang-ff1a-mo-xing/di-jiu-jieff1a-manager-dui-xiang.html)

### makemigrations & migrate

* makemigrations

  * 如果makemigrations命令后面没有 跟着 app_name 那么makemigrations 默认生成所有app的迁移脚本，如果跟了，那么就只生成对应app的迁移脚本
  * --name 可以给迁移脚本指定一个名字

  ~~~python
  python manage.py makemigrations app_name --name 'do_something'
  ~~~

* migrate

  migrate  做了两件事情

  * 第一件：将迁移脚本中的代码翻译成sql语句，然后执行这个sql语句
  * 第二件：将现在完成的事情(迁移)记录在`django_migrations`数据表中

  他会将代码中的迁移脚本跟`django_migrations`表中的迁移记录做对比，如果发现表中没有这个迁移脚本的记录，那么它就会执行这个迁移脚本。

* --fake: 只做migrate的第二件事情，将某一个迁移脚本的名字添加到`django_migrations`表中

  如果 `django_migrations` 表中的记录跟 丢失或者 或者跟迁移脚本不一致，就可以使用 `--fake`

  ~~~python
  python manage.py migrate app_name --fake
  ~~~


* --fake-initial: 将第一次生成的迁移脚本记录在数据库中，但不会真正执行脚本。
  * 如果数据库中的迁移记录和代码中的迁移脚本不一致，并且不知道具体哪里不一致，那么就可以使用`--fake-initial`

* 如果代码中的迁移脚本和数据表中的迁移记录实在太多，搞不清楚哦到底哪里有问题
  * 将之前的迁移脚本全部废弃不再使用，将出问题的app下的多有模型跟数据表中的保持一致，将`django_migrations`表中相关app的迁移记录全部删除，重新映射，之后使用 `--fake-initial`参数，将刚刚生成的迁移脚本，标记为已经完成，这些对应的表已经在数据库中存在了，并不需要再去真正执行映射

### 根据已有的表自动生成模型

* 使用 `python manage.py inspectdb`将表结构转换为模型，但是执行完的结果是在终端中显示的，要把结果导入文件需要执行`python manage.py inspectdb > models.py`，他会将结果导入到项目根目录下的models.py文件中
* 如果想呀转换  单个表  的结构称为django 模型，那么可以执行 `python manage.py inspectdb table_name > models.py`

* 将生成的模型移植到目标app中，修正模型的类名称，外键关联，Meta等，要注意的是，千万不要修改表明

* 遇到多对多模型，如果删除生成的中间表，那么一定要再做多对多关联，并且将中间表的表明跟数据库表明保持一致

  * 可以使用db_table=''在模型中指定表名
  * 也可以直接修改数据库中的表名

  ~~~python 
  Tags = models.MangToMangField('Tag', db_table='articles_tags')
  ~~~
  * 因为这些表已经在数据库中存在了，所以再我们使用`makemigrations`生成迁移脚本之后，不必执行`migrate`迁移，使用`--fake-initinal`将这个脚本加入迁移记录

  ~~~python
  python manage.py migrate tab_name --fake-initinal 
  ~~~

  

