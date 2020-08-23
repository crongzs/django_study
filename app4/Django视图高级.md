# Django视图高级

### 限制请求装饰器

django内置了许多常见的装饰器

* django.http.decorators.http.require_http_methods
* `django.views.decorators.http.require_GET`：这个装饰器相当于是`require_http_methods(['GET'])`的简写形式，只允许使用`GET`的`method`来访问视图。
* `django.views.decorators.http.require_POST`：这个装饰器相当于是`require_http_methods(['POST'])`的简写形式，只允许使用`POST`的`method`来访问视图。
* `django.views.decorators.http.require_safe`：这个装饰器相当于是`require_http_methods(['GET','HEAD'])`的简写形式，只允许使用相对安全的方式来访问视图。因为`GET`和`HEAD`不会对服务器产生增删改的行为。因此是一种相对安全的请求方式。

app4/views.py

~~~python
# --------------------- method 装饰器 ---------------------

from app4.models import MethodArticle
from django.views.decorators.http import require_http_methods, require_POST, require_GET, require_safe


# require_GET = require_http_methods(['GET'])
# require_safe = require_http_methods(['GET', 'POST'])
# require_POST = require_http_methods(['POST'])

# @require_http_methods(['GET'])
@require_GET
def method_get(request):
    ''' 限制为get请求 '''
    article = MethodArticle.objects.first()
    context = {
        'method': 'GET',
        'article': article
    }

    return render(request, 'app4/app4-1method.html', context=context)


# @require_http_methods(['POST'])
@require_POST
def method_post(request):
    ''' 限制为post请求 '''
    article = MethodArticle(title='Pthon', content='This is python', price=100.1).save()
    context = {
        'method': 'POST',
        'article': article
    }

    return render(request, 'app4/app4-1method.html', context=context)


# @require_safe
@require_http_methods(['GET', 'POST'])
def method_get_post(request):
    article = 'Django Request Method'
    method = 'Dont know'
    if request.method == 'GET':
        method = 'GET'
        article = MethodArticle.objects.first()

    if request.method == 'POST':
        method = 'POST'
        article = MethodArticle(title='Pthon', content='This is python', price=100.1)

    context = {
        'method': method,
        'article': article
    }

    return render(request, 'app4/app4-1method.html', context=context)
~~~

### 重定向

重定向分为永久性重定向和暂时性重定向，在页面上体现的操作就是浏览器会从一个页面自动跳转到另外一个页面。比如用户访问了一个需要权限的页面，但是该用户当前并没有登录，因此我们应该给他重定向到登录页面。

- 永久性重定向：http的状态码是301，多用于旧网址被废弃了要转到一个新的网址确保用户的访问，最经典的就是京东网站，你输入www.jingdong.com的时候，会被重定向到www.jd.com，因为jingdong.com这个网址已经被废弃了，被改成jd.com，所以这种情况下应该用永久重定向。
- 暂时性重定向：http的状态码是302，表示页面的暂时性跳转。比如访问一个需要权限的网址，如果当前用户没有登录，应该重定向到登录页面，这种情况下，应该用暂时性重定向。

在`Django`中，重定向是使用`redirect(to, *args, permanent=False, **kwargs)`来实现的。`to`是一个`url`，`permanent`代表的是这个重定向是否是一个永久的重定向，默认是`False`。

app4/views.py

~~~python
# --------------------- method 重定向 ---------------------
from django.shortcuts import redirect


def rediction_1(request):
    username = request.GET.get('username')
    if username:
        return HttpResponse('<h1>I have a username: %s</h1>' % username)
    else:
        return redirect('app4:app4-5')


def rediction_2(request):
    next = request.GET.get('next')
    if next:
        return render(request, 'app4/app4-2rediction.html', context={'username': 'ku_rong'})
    else:
        return HttpResponse('<h1>Dont have next url</h1>')
~~~

### WSGIRequest对象常用属性：

`WSGIRequest`对象上大部分的属性都是只读的。因为这些属性是从客户端上传上来的，没必要做任何的修改。以下将对一些常用的属性进行讲解：

1. `path`：请求服务器的完整“路径”，但不包含域名和参数。比如`http://www.baidu.com/xxx/yyy/`，那么`path`就是`/xxx/yyy/`。

2. `method`：代表当前请求的`http`方法。比如是`GET`还是`POST`。

3. `GET`：一个`django.http.request.QueryDict`对象。操作起来类似于字典。这个属性中包含了所有以`?xxx=xxx`的方式上传上来的参数。

4. `POST`：也是一个`django.http.request.QueryDict`对象。这个属性中包含了所有以`POST`方式上传上来的参数。

5. `FILES`：也是一个`django.http.request.QueryDict`对象。这个属性中包含了所有上传的文件。

6. `COOKIES`：一个标准的Python字典，包含所有的`cookie`，键值对都是字符串类型。

7. `session`：一个类似于字典的对象。用来操作服务器的`session`。

8. `META`：存储的客户端发送上来的所有`header`信息。

9. `CONTENT_LENGTH`：请求的正文的长度（是一个字符串）。

10. `CONTENT_TYPE`：请求的正文的MIME类型。

11. `HTTP_ACCEPT`：响应可接收的Content-Type。

12. `HTTP_ACCEPT_ENCODING`：响应可接收的编码。

13. `HTTP_ACCEPT_LANGUAGE`： 响应可接收的语言。

14. `HTTP_HOST`：客户端发送的HOST值。

15. `HTTP_REFERER`：在访问这个页面上一个页面的url。

16. `QUERY_STRING`：单个字符串形式的查询字符串（未解析过的形式）。

17. ```
    REMOTE_ADDR
    ```

    ：客户端的IP地址。如果服务器使用了

    ```
    nginx
    ```

    做反向代理或者负载均衡，那么这个值返回的是

    ```
    127.0.0.1
    ```

    ，这时候可以使用

    ```
    HTTP_X_FORWARDED_FOR
    ```

    来获取，所以获取

    ```
    ip
    ```

    地址的代码片段如下：

    ```python
      if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
          ip =  request.META['HTTP_X_FORWARDED_FOR']  
      else:  
          ip = request.META['REMOTE_ADDR']
    ```

18. `REMOTE_HOST`：客户端的主机名。

19. `REQUEST_METHOD`：请求方法。一个字符串类似于`GET`或者`POST`。

20. `SERVER_NAME`：服务器域名。

21. `SERVER_PORT`：服务器端口号，是一个字符串类型。

##### WSGIRequest对象常用方法：

1. `is_secure()`：是否是采用`https`协议。
2. `is_ajax()`：是否采用`ajax`发送的请求。原理就是判断请求头中是否存在`X-Requested-With:XMLHttpRequest`。
3. `get_host()`：服务器的域名。如果在访问的时候还有端口号，那么会加上端口号。比如`www.baidu.com:9000`。
4. `get_full_path()`：返回完整的path。如果有查询字符串，还会加上查询字符串。比如`/music/bands/?print=True`。
5. `get_raw_uri()`：获取请求的完整`url`。

app4/views.py

~~~python
# --------------------- WSGIRequest ---------------------
from django.core.handlers.wsgi import WSGIRequest


def wesgi_request(request):
    print(type(request))  # 结果：<class 'django.core.handlers.wsgi.WSGIRequest'>

    # 进入 django.core.handlers.wsgi.WSGIRequest

    '''
    class WSGIRequest(HttpRequest):
        def __init__(self, environ):
        ...
    
    1. WSGIRequest 继承自 HttpRequest
    '''
    # 获取浏览器发送过来的请求头
    print(request.META)
    # 获取url的完整路径
    print(request.path)  # 结果：/app4/wsgi-request/
    # 获取完整path(包括查询字符串)
    print(request.get_full_path())  # 结果：/app4/wsgi-request/?username=ku_rong
    # 获取完整的url(包括域名)
    print(request.get_raw_uri())  # 结果：http://127.0.0.1:8000/app4/wsgi-request/?username=ku_rong
    # 获取服务器域名
    print(request.get_host())  # 结果：127.0.0.1:8000
    # 判断是否使用https协议
    print(request.is_secure())  # 结果：False
    # 判断是否使用ajax发送请求
    print(request.is_ajax())  # 结果：False

    return HttpResponse('<h1>WSGIRequest</h1>')
~~~

### QueryDict对象：

我们平时用的`request.GET`和`request.POST`都是`QueryDict`对象，这个对象继承自`dict`，因此用法跟`dict`相差无几。其中用得比较多的是`get`方法和`getlist`方法。

1. `get`方法：用来获取指定`key`的值，如果没有这个`key`，那么会返回`None`。
2. `getlist`方法：如果浏览器上传上来的`key`对应的值有多个，那么就需要通过这个方法获取。

app4/views.py

~~~python
# --------------------- QueryDict对象 ---------------------


@require_http_methods(['GET', 'POST'])
def querydict(request):
    print(type(request.GET))  # result: <class 'django.http.request.QueryDict'>
    print(type(request.POST))  # result: <class 'django.http.request.QueryDict'>

    # request.GET 和 request.POST都属于 QueryDict对象

    # get()方法

    # username1 = request.GET['username']  # 以这种方式获取，如果没有值，那么就会报错
    username2 = request.GET.get('username', 'ku_rong')  # 以这种方式获取，如果没有值，他就会将默认值ku_rong返回

    # get_list() 获取某些key值，它对应的的数据有多个的情况，例如可多选的复选框
    if request.method == 'FET':
        title, content, tags = '', '', ''
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags = request.POST.getlist('tag')

    context = {
        'username': username2,
        'title': title,
        'content': content,
        'tags': tags
    }

    return render(request, 'app4/app4-3get_and_get_list.html', context=context)
~~~

templates/app4/app4-3get_or_getlist.html

~~~pythn
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>get and get_list</title>
</head>
<body>
    <h1>get() ---  hello {{ username }}</h1>
    <h1>getlist()</h1>
    <form action="" method="post">
        <table>
            <tbody>
            <tr>
                <td>title</td>
                <td>
                    <input type="text" name="title">
                </td>
            </tr>
            <tr>
                <td>content</td>
                <td>
                    <input type="text" name="content">
                </td>
            </tr>
            <tr>
                <td>Tag</td>
                <td>
                    <lable>
                        python
                        <input type="checkbox" name="tag" value="python">
                    </lable>
                </td>
                <td>
                    <labler>
                        django
                        <input type="checkbox" name="tag" value="django">
                    </labler>
                </td>
            </tr>
            <tr>
                <td>
                    <input type="submit" value="submit">
                </td>
            </tr>
            </tbody>
        </table>
    </form>
    {% if tags and title and content %}
        <h1>title: {{ title }}</h1>
        <h2>content:</h2>
        <h2>{{ content }}</h2>
        <h2>tags:</h2>
        <h2>{{ tags.0 }}, {{ tags.1 }}</h2>
    {% endif %}
</body>
</html>
~~~

### HttpResponse

Django服务器接收到客户端发送过来的请求后，会将提交上来的这些数据封装成一个`HttpRequest`对象传给视图函数。那么视图函数在处理完相关的逻辑后，也需要返回一个响应给浏览器。而这个响应，我们必须返回`HttpResponseBase`或者他的子类的对象。而`HttpResponse`则是`HttpResponseBase`用得最多的子类。

###### 常用属性：

1. content：返回的内容。

2. status_code：返回的HTTP响应状态码。

3. content_type：返回的数据的MIME类型，默认为

   ```
   text/html
   ```

   。浏览器会根据这个属性，来显示数据。如果是

   ```
   text/html
   ```

   ，那么就会解析这个字符串，如果

   ```
   text/plain
   ```

   ，那么就会显示一个纯文本。常用的

   ```
   Content-Type
   ```

   如下：

   - text/html（默认的，html文件）
   - text/plain（纯文本）
   - text/css（css文件）
   - text/javascript（js文件）
   - multipart/form-data（文件提交）
   - application/json（json传输）
   - application/xml（xml文件）

4. 设置请求头：`response['X-Access-Token'] = 'xxxx'`。

######常用方法：

1. set_cookie：用来设置`cookie`信息。后面讲到授权的时候会着重讲到。
2. delete_cookie：用来删除`cookie`信息。
3. write：`HttpResponse`是一个类似于文件的对象，可以用来写入数据到数据体（content）中。

###### JsonResponse类：

用来对象`dump`成`json`字符串，然后返回将`json`字符串封装成`Response`对象返回给浏览器。并且他的`Content-Type`是`application/json`。示例代码如下：

```python
from django.http import JsonResponse
def index(request):
    return JsonResponse({"username":"zhiliao","age":18})
```

默认情况下`JsonResponse`只能对字典进行`dump`，如果想要对非字典的数据进行`dump`，那么需要给`JsonResponse`传递一个`safe=False`参数。示例代码如下：

```python
from django.http import JsonResponse
def index(request):
    persons = ['张三','李四','王五']
    return HttpResponse(persons)
```

以上代码会报错，应该在使用`HttpResponse`的时候，传入一个`safe=False`参数，示例代码如下：

```python
return HttpResponse(persons,safe=False)
```

app4/views.py

~~~python
import json
from django.http import JsonResponse


def jsonresponse(request):
    ku_rong = {
        'name': 'ku_rong',
        'age': 18,
    }

    # 使用普通方法发送json数据
    # ku_rong = json.dumps(ku_rong)
    # response = HttpResponse(ku_rong, content_type='application/json')
    # return response

    # 使用 JsonResponse 发送json数据
    # response = JsonResponse(ku_rong)
    # return response

    # 默认情况下 JsonResponse 只能对字典进行 dumps ，如果要对其他类型的数据 如 列表list 进行dumps 需要传递一个 safe=False 参数才行
    fruit = ['apple', 'almod', 'blackbreey', 'bluebreey']
    response = JsonResponse(fruit, safe=False)
    return response
~~~

### 生成CSV文件

##### 生成小的csv

* 使用python内置的csv模块生成

~~~python
# --------------------- 生成CSV文件 ---------------------

import csv


def csv1(request):
    response = HttpResponse(content_type='text/csv')
    # 设置headers
    response['Content-Disposition'] = "attachment;filename=abc.csv"
    # response 实现了一个方法 write，因此可以将数据写入到response中

    writer = csv.writer(response)
    writer.writerow(['username', 'age'])
    writer.writerow(['ku_rong', '18'])
    return response


from django.template import loader
~~~

* 使用模版生成

~~~python
def csv2(request):
    ''' 使用模版创建csv文件 '''
    response = HttpResponse(content_type='text/csv')
    # 设置headers
    response['Content-Disposition'] = "attachment;filename=abc.csv"

    # 内容
    context = {
        'rows': [['username', 'age'], ['ku_rong', 18]]
    }
    # 加载模版
    template = loader.get_template('app4/app4.txt')
    csv = template.render(context=context)

    response.content = csv

    return response
~~~



##### 生成大的csv

###### 关于StreamingHttpResponse

这个类是专门处理流数据的，使得在处理一些大型文件的时候，不会因为服务器处理时间长而连接超时。

* 这个类没有 contetn 相反是 streaming_content
* 这个类的 streaming_content 必须是一个可以迭代的对象
* 这个类没有 write 方法，如果给这个类写入数据会报错
* 这个类不是继承自 Httpresponse
* 它会启动一个进程和客户端保持连接，所以很耗费资源，因此不是特殊要求尽量要少用

### 类视图

##### TemplateView

**django.views.generic.base.TemplateView**，这个类视图是专门用来返回模版的。在这个类中，有两个属性是经常需要用到的，一个是`template_name`，这个属性是用来存储模版的路径，`TemplateView`会自动的渲染这个变量指向的模版。另外一个是`get_context_data`，这个方法是用来返回上下文数据的，也就是在给模版传的参数的。

app4/urls.py

~~~python
 # ---------------- TemplateView ----------------
    # 如果渲染的这个模版不需要传递任何参数，那么建议在url中使用TemplateView
    path('TemplateView/', TemplateView.as_view(template_name='app4/app4-4TemplateView.html'), name='app4-13'),
    # 如果即想使用 TemplateView 又想给模版提供参数呢
    path('TemplateViewAbout/', views.TemplateViewContent.as_view(), name='app4-14')
~~~

app4/views.py

~~~python
# --------------------- 类视图 ---------------------
from django.views.generic import View, TemplateView


class TemplateViewContent(TemplateView):
    '''
    TemplateView 这个类视图是专门用来返回模版的，
    单独使用 TemplateView 只需要在urls.py 中直接映射即可，但不能够向模版传递参数

    如果既想使用 TemplateView 又想给模版传递参数，
    那么就需要继承 TemplateView 重写一个类视图

    '''

    # 必须要指定 template_name
    template_name = 'app4/app4-4TemplateView.html'

    # 必须定义 get_context_data() 方法
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'ku_rong'
        return context
~~~

##### ListView

在网站开发中，经常会出现需要列出某个表中的一些数据作为列表展示出来。比如文章列表，图书列表等等。在`Django`中可以使用`ListView`来帮我们快速实现这种需求。

app4/views.py

~~~python
# --------------------- TemplateView ---------------------
from django.views.generic import ListView
from app4.models import ViewArticel


class ArticleListView(ListView):
    # 指定这个列表是给哪个模型的
    model = ViewArticel
    # 指定这个列表的模板
    template_name = 'app4/app4-5ListView.html'
    # 指定这个列表一页中展示多少条数据
    paginate_by = 10
    # 指定这个列表的排序方式
    ordering = 'created'
    # 获取第几页的数据的参数名称。默认是page。
    page_kwarg = 'page'
    # 指定这个列表模型在模板中的参数名称
    context_object_name = 'articles'

    # 获取上下文的数据
    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        print(context)
        return context

    # 如果你提取数据的时候，并不是要把所有数据都返回，那么你可以重写这个方法。将一些不需要展示的数据给过滤掉。
    def get_queryset(self):
        return ViewArticel.objects.all()
~~~

###### Paginator和Page类

`Paginator`和`Page`类都是用来做分页的。他们在`Django`中的路径为`django.core.paginator.Paginator`和`django.core.paginator.Page`。

###### Paginator常用属性和方法：

1. `count`：总共有多少条数据。
2. `num_pages`：总共有多少页。
3. `page_range`：页面的区间。比如有三页，那么就`range(1,4)`。

###### Page常用属性和方法：

1. `has_next`：是否还有下一页。
2. `has_previous`：是否还有上一页。
3. `next_page_number`：下一页的页码。
4. `previous_page_number`：上一页的页码。
5. `number`：当前页。
6. `start_index`：当前这一页的第一条数据的索引值。
7. `end_index`：当前这一页的最后一条数据的索引值。

app4/views.py

~~~python
# --------------------- TemplateView ---------------------
from django.views.generic import ListView
from app4.models import ViewArticel


class ArticleListView(ListView):
    # 指定这个列表是给哪个模型的
    model = ViewArticel
    # 指定这个列表的模板
    template_name = 'app4/app4-5ListView.html'
    # 指定这个列表一页中展示多少条数据
    paginate_by = 5
    # 指定这个列表的排序方式
    ordering = 'created'
    # 获取第几页的数据的参数名称。默认是page。
    page_kwarg = 'page'
    # 指定这个列表模型在模板中的参数名称
    context_object_name = 'articles'

    # 获取上下文的数据
    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['lift'] = context.get('page_obj').number - 2
        context['right'] = context.get('page_obj').number + 2
        return context

    # 如果你提取数据的时候，并不是要把所有数据都返回，那么你可以重写这个方法。将一些不需要展示的数据给过滤掉。
    def get_queryset(self):
        return ViewArticel.objects.all()
~~~

template/app4/app4-5ListView.html

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ListView</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css"
          integrity="sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB" crossorigin="anonymous">

</head>
<body>
<ul>
    {% for article in articles %}
        <li>{{ article.title }} {{ article.content }}</li>
    {% endfor %}
</ul>

<nav aria-label="Page navigation example">
    <ul class="pagination">
        {% if page_obj.has_previous %}
            <li class="page-item"><a class="page-link" href="{% url 'app4:app4-15' %}?page={{ page_obj.previous_page_number }}">Previous</a></li>
        {% else %}
            <li class="page-item disabled"><a class="page-link" href="#">Previous</a></li>
        {% endif %}
        {% if lift <= 1 %}

        {% else %}
            <li class="page-item"><a class="page-link" href="{% url 'app4:app4-15' %}?page=1">1</a></li>
            <li class="page-item disabled"><a class="page-link" href="#">...</a></li>
        {% endif %}


        {% for page in paginator.page_range %}
            {% if page == page_obj.number %}
                <li class="page-item active"><a class="page-link" href="{% url 'app4:app4-15' %}?page={{ page }}">{{ page }}</a></li>
            {% elif page >= lift and page <= right %}
                <li class="page-item"><a class="page-link" href="{% url 'app4:app4-15' %}?page={{ page }}">{{ page }}</a></li>
            {% else %}
            {% endif %}
        {% endfor %}

        {% if right >= paginator.num_pages %}
        {% else %}
            <li class="page-item disabled"><a class="page-link" href="#">...</a></li>
            <li class="page-item"><a class="page-link" href="{% url 'app4:app4-15' %}?page={{ paginator.num_pages }}">{{ paginator.num_pages }}</a></li>
        {% endif %}
        {% if page_obj.has_next %}
            <li class="page-item"><a class="page-link" href="{% url 'app4:app4-15' %}?page={{ page_obj.next_page_number }}">Next</a></li>
        {% else %}
            <li class="page-item disabled"><a class="page-link" href="#">Next</a></li>
        {% endif %}

    </ul>
</nav>
</body>
</html>
~~~

### 给类视图添加装饰器



app4/views.py

~~~python
# --------------------- 给类视图添加装饰器 ---------------------
from django.utils.decorators import method_decorator

'''
两种方法装饰
1. 在dispach()方法上装饰，但是我们不会总是重写 dispath方法，因此这种方式不建议使用
2. 直接可以装饰在类上面，但是 要指定装饰的方法是dispatch
'''


# 定义一个装饰器
def info_user(func):
    def wrapper(request, *args, **kwargs):
        username = request.GET.get('username')

        if username:
            return func(request, *args, **kwargs)
        else:
            return redirect('app4:app4-15')

    return wrapper


@method_decorator(info_user, name='dispatch')  # 第二种装饰方法
class ArticlesView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('<hq>在 dispatch 上添加装饰器</h1>')

    # 第一种装饰方法
    # django 之中，如果要装饰一个方法的话，Django 提供了一个 装饰器 method_decorator 可以使装饰方法变得安全
    @method_decorator(info_user)
    def dispatch(self, request, *args, **kwargs):
        return super(ArticlesView, self).dispatch(request, *args, **kwargs)
~~~

### 状态码错误处理

* 直接在`templates.py`文件夹中创建`404.html`、`500.html`，当服务器发生错误时，Django会自动映射到这些页面。⚠️：保证`DEBUG=Fasle`
* 除404、500以外的错误处理，可以专门配置一个存放错误页面的app进行管理映射

error/views.py

~~~python
from django.shortcuts import render


def error_403(request):
    return render(request, 'error/403.html')


def error_405(request):
    return render(request, 'error/405.html')

~~~

error/urls.py

~~~python
from django.urls import path

from error import views

app_name = 'error'

urlpatterns = [
    path('403/', views.error_403, name='403'),
    path('405/', views.error_405, name='405'),
]

~~~

