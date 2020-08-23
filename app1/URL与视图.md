# Django URL 与视图函数

### 视图

视图一般都写在`app`的`views.py`中。并且视图的第一个参数永远都是`request`（一个HttpRequest）对象。这个对象存储了请求过来的所有信息，包括携带的参数以及一些头部信息等。在视图中，一般是完成逻辑相关的操作。比如这个请求是添加一篇博客，那么可以通过request来接收到这些数据，然后存储到数据库中，最后再把执行的结果返回给浏览器。视图函数的返回结果必须是`HttpResponseBase`对象或者子类的对象。示例代码如下：

~~~python
from django.http import HttpResponse
def book_list(request):
    return HttpResponse("书籍列表！")
~~~

### URL映射

在`setting.py`中配置了`ROOT_URLCONF`为`urls.py`,所以django会去`urls.py`中寻找

### URL中添加参数

urls.py

~~~python
from django.urls import path

from app1 import views

app_name = 'd1_rul'

urlpatterns = [
    ...
    # url中传递参数给视图函数
    path('args-1/<int:id>/', views.url_args1, name='args-1'),
    path('args-2/', views.url_args2, name='args-2'),
]
~~~

views.py

~~~python
from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse


def url_args1(request, id):
    '''
    在URL中使用变量的方式传递参数
    '''
    return HttpResponse('<h1>URL1 ID is {} </h1>'.format(id))


def url_args2(request):
    '''
    以查询字符串的形式传递参数
    '''
    id = request.GET.get('id')
    return HttpResponse('<h1>URL2 ID is {} </h1>'.format(id))
~~~

### URL转换器

`django.urls.converters`中定义了`Django`内置的所有`URL`转换器

* int：只有一个或者多个的阿拉伯数字
* str：除了斜杠`/`以外的所有字符串都是可以的
* path：所有字符串都满足
* uuid：只满足uuid格式的字符串
* slug：英文中的横杠或者英文字符或者阿拉伯数字或者下划线才满足

### URL模块化

随着项目的越来越大，url的数量也会增大，为了方便管理url，需要将每个app对应的url独立管理，这就是url模块化，实现URl模块化需要借助`include`函数

~~~python
from django.urls import path, include

urlpatterns = [
    ...
    path('app1/', include('app1.urls')),
]
~~~

### URL命名与URL反转

`django.urls.path`函数中的name参数为URL命名

`django.shortcuts.reverse`函数实现URL反转

在项目复杂的时候URL命名与URL反转的作用很大，在使用URL命名和URL反转时，首先将 app 在 `settings.py`中的`INSTALLED_APPS`中进行注册，然后app对应的`urls.py`中定义变量 `app_name=app的名称`，`app_name`将作为应用命名空间变量区分不同app中出现相同的URL命名的情况。

settings.py

~~~python
...
INSTALLED_APPS = [
    ...
    'app1',
]
...
~~~

app1/urls.py

~~~python
...
app_name = 'app1'
...
~~~

* url命名

app1/urls.py

~~~python
from django.urls import path
from django.urls import converters

from app1 import views

app_name = 'app1'

urlpatterns = [
   ...
    # url命名与url反转
    path('args-3/', views.url_args3, name='args-3'),
    path('args-4/', views.url_args4, name='args-4'),
    path('args-5/', views.url_args5, name='args-5'),

]
~~~

* URL反转

app1/views.py

~~~python
# ------------------- URL命名与URL反转 -------------------


def url_args3(request):
    username = request.GET.get('username')
    if username:
        return HttpResponse('<h1>This isi URL3, username is {}</h1>'.format(username))
    else:
        return redirect('/args-4/')


def url_args4(request):
    return HttpResponse('<h1>This is URL4</h1>')


def url_args5(request):
    '''使用reverse函数 根据URLname 实现URL反转'''
    username = request.GET.get('username')
    if username:
        return HttpResponse('<h1>This isi URL3, username is {}</h1>'.format(username))
    else:
        return redirect(reverse('app1:args-4'))  # ‘app_name:name’
~~~

### 实例命名空间

实例命名空间是为了区分在 主`urls.py`中出现一个同一个 app 下有两个实例的情况，因此在`include`函数中添加参数`namespace=不同实例名`，以区分不同的实例。

* ⚠️注意：要指定一个实例命名空间`namespace`必须先指定一个应用命名空间`app_name`

urls.py

~~~python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    ...

    # ------------- URL与视图 -------------
    path('app1/', include('app1.urls', namespace='app1-a')),
    # 实例命名空间: 同一个app1下出现了两个实例app1、app1-1
    path('app1-1/', include('app1.urls', namespace='app1-b')),

]
~~~

app1/views.py

~~~python
# ------------------- 实例命名空间 -------------------


def url_args6(request):
    username = request.GET.get('username')
    if username:
        return HttpResponse('<h1>This isi URL6, username is {}</h1>'.format(username))
    else:
        current_namespace = request.resolver_match.namespace  # 获取当前实例名称
        return redirect(reverse('%s:args-7'%current_namespace))


def url_args7(request):
    return HttpResponse('<h1>This is URL7</h1>')
~~~

* `include((pattern,app_namespace),namespace=None)`：在包含某个`app`的`urls`的时候，可以指定命名空间，这样做的目的是为了防止不同的`app`下出现相同的`url`，这时候就可以通过命名空间进行区分。

~~~python
 from django.contrib import admin
 from django.urls import path,include

 urlpatterns = [
     path('admin/', admin.site.urls),
     path('book/',include(("book.urls",'book')),namespace='book')
 ]
~~~

### 将 子URL放到 inclued 中

urls.py

~~~python
from django.contrib import admin
from django.urls import path, include

from app1 import inclued_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('app1.urls')),

    # ------------- URL与视图 -------------
    path('app1/', include('app1.urls', namespace='app1-a')),
    # 实例命名空间: 同一个app1下出现了两个实例app1、app1-1
    path('app1-1/', include('app1.urls', namespace='app1-b')),
    # 将 子URL 放到 include 中
    path('app1-2/', include([
        path('include/', inclued_views.app1_inclued, name='include_path')
    ]))
]
~~~

app1/inclued_views.py

~~~python
from django.http import HttpResponse


def app1_inclued(request):
    return HttpResponse('<h1>This is Include path</h1>')

~~~

### re_path

`re_path` 和 `path` 的作用是一样的，只不过`re_path`在写 url 的时候可以使用正则表达式，功能更加强大

使用`re_path`写url时建议使用原生字符写正则表达式，也就是以`r`开头的字符串

app1/urls.py

~~~python
from django.urls import path, re_path
from django.urls import converters

from app1 import views

app_name = 'app1'

urlpatterns = [
  	...
    # 使用re_path
    re_path(r're_path/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/', views.url_args8, name='re-path')
]

~~~

app1/views.py

~~~python
def url_args8(request, year, month):
    ''' re_path 的使用'''
    return HttpResponse('<h1>This is URL8 {}-{}</h1>'.format(year, month))
~~~

### URL反转添加参数

如果在反转url的时候需要添加参数，那么可以传递kwargs参数到revers函数

如果想要添加查询字符串参数，则必须手动进行字符串拼接

app1/urls.py

~~~python
from django.urls import path, re_path
from django.urls import converters

from app1 import views

app_name = 'app1'

urlpatterns = [
    ...

    # url带参数反转
    path('args-9/', views.url_args9, name='args-9'),
    path('args-10/<int:id>/<int:page>/', views.url_args10, name='args-10'),

    # url携带查询字符串参数反转
    path('args-11/', views.url_args11, name='args-11'),
    path('args-12/', views.url_args12, name='args-12'),

]

~~~

app1/views.py

~~~python
def url_args9(request):
    '''URL带参数反转'''
    username = request.GET.get('username')
    if username:
        return HttpResponse('<h1>This is URL9 username is {}</h1>'.format(username))
    else:
        return redirect(reverse('app1-a:args-10', kwargs={'id': 1, 'page': 1}))


def url_args10(request, id, page):
    return HttpResponse('<h1>This is URL10, ID is {} Page is {}</h1>'.format(id, page))


def url_args11(request):
    '''url携带查询字符串参数反转'''
    app_name = request.resolver_match.url_name  # 获取应用命名空间
    return redirect(reverse('app1-a:args-12')+'?next={}'.format(app_name))


def url_args12(request):
    next = request.GET.get('next')
    return HttpResponse('<h1>This is URL next view is {}</h1>'.format(next))
~~~

### 自定义URL转换器

to_python 将参数在传到视图函数之前转换成 转换器 规定的类型 比如 转换器`<int: id>` 在参数到视图函数之前先将参数id转换成`int`类型

to_url 在revers反转的时候将 kwargs中的参数做处理，然后传递到url拼接成完整的url 比如 `reverse('app1-a:args-10', kwargs={'id': 1, 'page': 1})` , `to_url`会将 kwargs 中的参数进行处理再拼接成url



1. 定义一个类，继承object
2. 在类中第一个属性regex，这个属性是用来限制url参数的规则的正则表达式，名称必须是regex，不然django不会识别
3. 实现`to_python`方法，这个方法将url中的参数转换为视图函数需要的类型，传递给视图函数
4. 实现`to_url`方法，这个方法是在`revers`函数反转url的时候将参数转换后拼接成一个正确的url
5. 将定义好的转换器类通过`django.urls.register_converter`注册到Django中

app1/urls.py

~~~python
from django.urls import path, re_path
from django.urls import converters, register_converter


class CategoryConverter(object):
    regex = r'\w+|(\w+\+\w+)+'  # 这里的正则表达式 变量名称 必须是 regex 不然Django不能识别

    def to_python(self, value):
        '''
        将 python+django+flask 处理成 ['python', 'django', 'flask']
        '''
        result = value.split('+')
        return result

    def to_url(self, value):
        '''
        将 ['python', 'django', 'flask'] 处理成 python+django+flask
        '''
        if isinstance(value, list):
            result = '+'.join(value)
            return result
        else:
            raise RuntimeError('转换URL的时候分类参数必须为list类型')


register_converter(CategoryConverter, 'cate')  # 将自定义的转换通过 register_converter 器注册到 Django 命名为 cate


from app1 import views

app_name = 'app1'

urlpatterns = [
  	...
    # 自定义path转换器
    path('args-13/<cate:categories>/', views.url_args13, name='args-13'),
    path('args-14/', views.url_args14, name='args-14'),

]

~~~

app1/views.py

~~~python
# ------------------- URL带参数反转 -------------------


def url_args13(request, categories):
    '''自定义path转化器的 to_python 将 python+django+flask 处理成 ['python', 'django', 'flask'] '''
    return HttpResponse('<h1>This is URL13 categories is {}</h1>'.format(categories))


def url_args14(request):
    '''自定义path转化器的 to_url 将 ['python', 'django', 'flask'] 处理成 python+django+flask '''
    List = ['python', 'django', 'flask']
    url = reverse('app1:args-13', kwargs={'categories': List})
    print('url:', url)
    return redirect(url)
~~~

### 指定默认参数

app1/urls.py

~~~python
...

urlpatterns = [
    ...
    # URL映射的时候指定默认参数
    path('args-15/<int:page>/', views.url_args15, name='args-15'),
    path('args-15-1/', views.url_args15, name='args-15-1'),

]

~~~

app1/views.py

~~~python
# ------------------- URL映射指定默认参数 -------------------

def url_args15(request, page=1):
    ''' 在视图函数中指定默认参数 '''
    return HttpResponse('<h1>This is URL15 Page is {} </h1>'.format(page))
~~~

