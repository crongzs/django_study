# Django 模版

### 模版渲染

* `render_to_string`找到模板，然后将模板编译后渲染成Python的字符串格式。最后再通过`HttpResponse`类包装成一个`HttpResponse`对象返回回去。示例代码如下：

* 以上方式虽然已经很方便了。但是django还提供了一个更加简便的方式，直接将模板渲染成字符串和包装成`HttpResponse`对象一步到位完成。示例代码如下：

app2/views.py

~~~python
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string


def template1(request):
    ''' render_to_string 渲染模版 '''
    html = render_to_string('app2-1.html')
    return HttpResponse(html)


def template2(request):
    ''' render 渲染模版'''
    return render(request, 'app2-1.html')
~~~

app2/urls.py

~~~python
from django.urls import path

from app2 import views

app_name = 'app2'

urlpatterns = [
    # 模版渲染的两种方式
    path('template1/', views.template1, name='app2-1'),
    path('template2/', views.template2, name='app2-2'),
]

~~~

### 模版查找的路径配置

所有和模版相关的配置都会设置在`settings.py`中的`TEMPLATES`中

setting.py

~~~python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # django模版的查找路径
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # 设置为True表示django除了去DIRS里面的路径查找模版文件，还会去app下面查找templates(app必须在INSTALLED_APPS中注册)
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
~~~

1. `DIRS`：这是一个列表，在这个列表中可以存放所有的模板路径，以后在视图中使用`render`或者`render_to_string`渲染模板的时候，会在这个列表的路径中查找模板。
2. `APP_DIRS`：默认为`True`，这个设置为`True`后，会在`INSTALLED_APPS`的安装了的`APP`下的`templates`文件加中查找模板。
3. 查找顺序：比如代码`render('list.html')`。先会在`DIRS`这个列表中依次查找路径下有没有这个模板，如果有，就返回。如果`DIRS`列表中所有的路径都没有找到，那么会先检查当前这个视图所处的`app`是否已经安装，如果已经安装了，那么就先在当前这个`app`下的`templates`文件夹中查找模板，如果没有找到，那么会在其他已经安装了的`app`中查找。如果所有路径下都没有找到，那么会抛出一个`TemplateDoesNotExist`的异常。

### 模版变量使用

django.shortcuts.render

~~~python
def render(request, template_name, context=None, content_type=None, status=None, using=None):
    """
    Return a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    content = loader.render_to_string(template_name, context, request, using=using)
    return HttpResponse(content, content_type, status)
~~~

* context参数 上下文 专门用来存储参数，必须为一个字典类型

* 模板中的变量同样也支持`点(.)`的形式。在出现了点的情况，比如`person.username`，模板是按照以下方式进行解析的：

1. 如果`person`是一个字典，那么就会查找这个字典的`username`这个`key`对应的值。
2. 如果`person`是一个对象，那么就会查找这个对象的`username`属性，或者是`username`这个方法。
3. 如果出现的是`person.1`，会判断`persons`是否是一个列表或者元组或者任意的可以通过下标访问的对象，如果是的话就取这个列表的第1个值。如果不是就获取到的是一个空的字符串。

app2/views.py

~~~python
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string


def template3(request):
    ''' 模版变量的使用'''

    persion = Persion('Rong Ku')  # 传递一个对象
    ku_rong = {
        'age': 18
    }  # 传递一个字典
    like1 = ['python', 'django']  # 传递一个列表
    like2 = ('movie', 'kendo')  # 传递一个元组

    context = {
        'username': 'ku_rong',
        'persion': persion,
        'ku_rong': ku_rong,
        'like1': like1,
        'like2': like2
    }
    return render(request, 'app2/app2-2.html', context=context)


class Persion(object):
    def __init__(self, username):
        self.name = username

~~~

app2/urls.py

~~~python
from django.urls import path

from app2 import views

app_name = 'app2'

urlpatterns = [
    ...
    # 模版变量的使用
    path('template3/', views.template3, name='app2-3'),
]

~~~

templates/app2/app2-2.html

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>模版变量的使用</title>
</head>
<body>
    <h1>hello {{ username }}</h1>
  {# persion.name 获取对象的属性， ku_rong.age 获取字典的value， like1.1，like2.0 获取字典和元组中的值 #}
    <h2>hello, my name is {{ persion.name }}, {{ ku_rong.age }} years old, like {{ like1.1 }} and {{ like2.0 }}</h2>
</body>
</html>
~~~

### for标签的使用

app2/views.py

~~~python
# ------------------------ for标签 ------------------------


def template4(request):
    context = {
        'examples': ['python', 'django', 'flask'],
        'persion': {
            'name': 'ku_rong',
            'age': 18,
            'work': 'coder'
        },
        'books': [
            {
                'name': '三国演义',
                'author': '罗贯中',
                'price': 120
            },
            {
                'name': '水浒传',
                'author': '施耐庵',
                'price': 100
            },
            {
                'name': '西游记',
                'author': '吴承恩',
                'price': 90
            },
            {
                'name': '红楼梦',
                'author': '曹雪芹',
                'price': 110
            },
        ],
        'comments': []
    }
    return render(request, 'app2/app2-3for标签.html', context=context)

~~~

app2/.urls.py

~~~python
from django.urls import path

from app2 import views

app_name = 'app2'

urlpatterns = [
  ...
    # for标签的使用
    path('template4/', views.template4, name='app2-4'),
]
~~~

templates/app2/app2-3for标签.html

~~~html
{% for book in books %}
		<li>{{ book }}</li>
{% endfor %}
~~~

* 反向遍历

~~~html
{% for book in books reversed%}
		<li>{{ book }}</li>
{% endfor %}
~~~

* 遍历字典

~~~html
{% for key, value in persion.items %}
		<li>{{ key }} : {{ value }}</li>
{% endfor %}

{% for key in persion.keys %}
		<li>{{ key }}</li>
{% endfor %}

{% for value in persion.values %}
		<li>{{ value }}</li>
{% endfor %}
~~~

- 在`for`循环中，`DTL`提供了一些变量可供使用。这些变量如下：
  - forloop.counter`：当前循环的下标。以1作为起始值。
  - `forloop.counter0`：当前循环的下标。以0作为起始值。
  - `forloop.revcounter`：当前循环的反向下标值。比如列表有5个元素，那么第一次遍历这个属性是等于5，第二次是4，以此类推。并且是以1作为最后一个元素的下标。
  - `forloop.revcounter0`：类似于forloop.revcounter。不同的是最后一个元素的下标是从0开始。
  - `forloop.first`：是否是第一次遍历。
  - `forloop.last`：是否是最后一次遍历。
  - `forloop.parentloop`：如果有多个循环嵌套，那么这个属性代表的是上一级的for循环。

~~~html
    <h1>其它用法</h1>
    <table>
        <thead>
        <tr>
            <td>subscript</td>
            <td>name</td>
            <td>author</td>
            <td>price</td>
        </tr>
        </thead>
        <tbody>
            {% for book in books %}
                <tr>
                    <td>{{ forloop.counter }}</td>
                    <td>{{ book.name }}</td>
                    <td>{{ book.author }}</td>
                    <td>{{ book.price }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
    <table>
        <thead>
        <tr>
            <td>subscript</td>
            <td>name</td>
            <td>author</td>
            <td>price</td>
        </tr>
        </thead>
        <tbody>
            {% for book in books %}
                <tr>
                    <td>{{ forloop.counter0 }}</td>
                    <td>{{ book.name }}</td>
                    <td>{{ book.author }}</td>
                    <td>{{ book.price }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
    <table>
        <thead>
        <tr>
            <td>subscript</td>
            <td>name</td>
            <td>author</td>
            <td>price</td>
        </tr>
        </thead>
        <tbody>
            {% for book in books reversed %}
                <tr>
                    <td>{{ forloop.revcounter }}</td>
                    <td>{{ book.name }}</td>
                    <td>{{ book.author }}</td>
                    <td>{{ book.price }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
    <table>
        <thead>
        <tr>
            <td>subscript</td>
            <td>name</td>
            <td>author</td>
            <td>price</td>
        </tr>
        </thead>
        <tbody>
            {% for book in books reversed %}
                <tr>
                    <td>{{ forloop.revcounter0 }}</td>
                    <td>{{ book.name }}</td>
                    <td>{{ book.author }}</td>
                    <td>{{ book.price }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
    <table>
        <thead>
        <tr>
            <td>subscript</td>
            <td>name</td>
            <td>author</td>
            <td>price</td>
        </tr>
        </thead>
        <tbody>
            {% for book in books reversed %}
                {% if forloop.first %}
                    <tr style="background: red;">
                {% elif forloop.last %}
                    <tr style="background: pink;">
                {% else %}
                    <tr>
                {% endif %}
                    <td>{{ forloop.revcounter0 }}</td>
                    <td>{{ book.name }}</td>
                    <td>{{ book.author }}</td>
                    <td>{{ book.price }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>

~~~

* `for...in...empty`标签：这个标签使用跟`for...in...`是一样的，只不过是在遍历的对象如果没有元素的情况下，会执行`empty`中的内容。示例代码如下

~~~python
    <ul>
        {% for comment in comments %}
            <li>{{ comment }}</li>
        {% empty %}
            <li>没有任何评论</li>
        {% endfor %}

    </ul>
~~~

### with 标签的用法

`with`标签：在模版中定义变量。有时候一个变量访问的时候比较复杂，那么可以先把这个复杂的变量缓存到一个变量上，以后就可以直接使用这个变量就可以了。

模版中通过with标签定义的变量，只能在with语句块中使用

app2/views.py

~~~python
# ------------------------ for标签 ------------------------


def template5(request):
    context = {
        'persons': ['ku_rong', 'ronggege']
    }
    return render(request, 'app2/app2-5with标签.html', context=context)
~~~

app2/urls.py

~~~python
from django.urls import path

from app2 import views

app_name = 'app2'

urlpatterns = [
  ...
    # 标签的使用
    path('template5/', views.template5, name='app2-5'),
]
~~~

templates/app2/app2-5with标签.html

~~~html
		<h1>with 标签的用法</h1>
    {% with shuaide=persons.1  %}
        <p>{{ shuaide }}</p>
    {% endwith %}

    {% with persons.0 as zuishuaide %}
        <p>{{ zuishuaide }}</p>
    {% endwith %}
~~~

### URL标签的使用

app2/views.py

~~~python
# ------------------------ url标签 ------------------------


def template6(request):
    context = {'page': 9, 'id': '001'}
    return render(request, 'app2/app2-6url标签.html', context=context)


def template7(request, id, page):
    context = {
        'id': id,
        'page': page,
        'next_url': reverse('app2:app2-6')
    }
    return render(request, 'app2/app2-7url标签.html', context=context)


def template8(request):
    next = request.GET.get('next')
    context = {'next': next}
    return render(request, 'app2/app2-8url标签.html', context=context)
~~~

app2/urls.py

~~~python
from django.urls import path

from app2 import views

app_name = 'app2'

urlpatterns = [
  ...
  # url标签的使用
  path('template6/', views.template6, name='app2-6'),
  path('template7/<str:id>/<int:page>/', views.template7, name='app2-7'),
  path('template8/', views.template8, name='app2-8'),

]

~~~

templates/app2/app2-6url标签.html

如果`url`反转的时候需要传递参数，那么可以在后面传递。但是参数分位置参数和关键字参数。位置参数和关键字参数不能同时使用

~~~html
# 关键字参数
{% with page=page id=id %}
  <p><a href="{% url 'app2:app2-7' id=id page=page %}">带参数跳转</a></p>
{% endwith %}

# 位置参数
  <p><a href="{% url 'app2:app2-7' id %}">带参数跳转</a></p>
~~~

templates/app2/app2-7url标签.html

使用`url`标签反转的时候要传递查询字符串的参数

~~~html
<p><a href="{% url 'app2:app2-8' %}?next={{ next_url }}">查询字符串跳转</a></p>
~~~

templates/app2/app2-8url标签.html

~~~html
<p><a href="{{ next }}">一般跳转</a></p>
~~~

### autoescape标签的使用

`autoescape`标签：开启和关闭这个标签内元素的自动转义功能。自动转义是可以将一些特殊的字符。比如`<`转义成`html`语法能识别的字符，会被转义成`<`，而`>`会被自动转义成`>`。模板中默认是已经开启了自动转义的

如果不知道自己是在干什么，最好使用DTL的自动转移，这样网站才不容易出现XSS泄漏，如果变量是可信任的，可以通过`autoescape`关闭自动转义

app2/views.py

~~~python
# ------------------------ autoescape标签 ------------------------

def template9(request):
    context = {
        'url': "<p><a href='https://www.baidu.com/'>百度</a></p>"
    }
    return render(request, 'app2/app2-9autoescape标签.html', context=context)
~~~

app2/urls.py

~~~python
from django.urls import path

from app2 import views

app_name = 'app2'

urlpatterns = [
  ...
  # autoescape标签的使用
  path('template9/', views.template9, name='app2-9'),

]
~~~

templates/app2/app2-9autoescape标签.html

~~~html
    <h1>autoescape 标签</h1>
    <p>模板中默认是已经开启了自动转义的</p>
    <p>{{ url }}</p>
    <p>关闭自动转义</p>
    {% autoescape off %}
        <p>{{ url }}</p>
    {% endautoescape %}
~~~

### verbatim标签的使用

`verbatim`标签：默认在`DTL`模板中是会去解析那些特殊字符的。比如`{%`和`%}`以及`{{`等。如果你在某个代码片段中不想使用`DTL`的解析引擎。那么你可以把这个代码片段放在`verbatim`标签中。

app2/views.py

~~~python
# ------------------------ verbatim标签 ------------------------

def template10(request):
    context = {
        'hello': 'ku_rong'
    }
    return render(request, 'app2/app2-10verbatim标签.html', context=context)
~~~

app2/urls.py

~~~python
from django.urls import path

from app2 import views

app_name = 'app2'

urlpatterns = [
  ...
  # verbatim标签的使用
  path('template10/', views.template10, name='app2-10'),

]

~~~

templates/app2/app2-9autoescape标签.html

~~~html
<h1>verbatim标签</h1>
{% verbatim %}
<p>{{ hello }}</p>
{% endverbatim %}
~~~

### 模版常用过滤器

在模版中，有时候需要对一些数据进行处理以后才能使用。一般在`Python`中我们是通过函数的形式来完成的。而在模版中，则是通过过滤器来实现的。过滤器使用的是`|`来使用。比如使用`add`过滤器，那么示例代码如下：

```html
    {{ value|add:"2" }}
```

那么以下就讲下在开发中常用的过滤器。

* add

将传进来的参数添加到原来的值上面。这个过滤器会尝试将`值`和`参数`转换成整形然后进行相加。如果转换成整形过程中失败了，那么会将`值`和`参数`进行拼接。如果是字符串，那么会拼接成字符串，如果是列表，那么会拼接成一个列表。示例代码如下：

```python
{{ value|add:"2" }}
```

如果`value`是等于4，那么结果将是6。如果`value`是等于一个普通的字符串，比如`abc`，那么结果将是`abc2`。`add`过滤器的源代码如下：

```python
def add(value, arg):
    """Add the arg to the value."""
    try:
        return int(value) + int(arg)
    except (ValueError, TypeError):
        try:
            return value + arg
        except Exception:
            return ''
```

* cut

移除值中所有指定的字符串。类似于`python`中的`replace(args,"")`。示例代码如下：

```python
{{ value|cut:" " }}
```

以上示例将会移除`value`中所有的空格字符。`cut`过滤器的源代码如下：

```python
def cut(value, arg):
    """Remove all values of arg from the given string."""
    safe = isinstance(value, SafeData)
    value = value.replace(arg, '')
    if safe and arg != ';':
        return mark_safe(value)
    return value
```

* date

将一个日期按照指定的格式，格式化成字符串。示例代码如下：

```python
# 数据
context = {
    "birthday": datetime.now()
}

# 模版
{{ birthday|date:"Y/m/d" }}
```

那么将会输出`2018/02/01`。其中`Y`代表的是四位数字的年份，`m`代表的是两位数字的月份，`d`代表的是两位数字的日。
还有更多时间格式化的方式。见下表。

| 格式字符 | 描述                                 | 示例  |
| -------- | ------------------------------------ | ----- |
| Y        | 四位数字的年份                       | 2018  |
| m        | 两位数字的月份                       | 01-12 |
| n        | 月份，1-9前面没有0前缀               | 1-12  |
| d        | 两位数字的天                         | 01-31 |
| j        | 天，但是1-9前面没有0前缀             | 1-31  |
| g        | 小时，12小时格式的，1-9前面没有0前缀 | 1-12  |
| h        | 小时，12小时格式的，1-9前面有0前缀   | 01-12 |
| G        | 小时，24小时格式的，1-9前面没有0前缀 | 1-23  |
| H        | 小时，24小时格式的，1-9前面有0前缀   | 01-23 |
| i        | 分钟，1-9前面有0前缀                 | 00-59 |
| s        | 秒，1-9前面有0前缀                   | 00-59 |

* default

如果值被评估为`False`。比如`[]`，`""`，`None`，`{}`等这些在`if`判断中为`False`的值，都会使用`default`过滤器提供的默认值。示例代码如下：

```python
{{ value|default:"nothing" }}
```

如果`value`是等于一个空的字符串。比如`""`，那么以上代码将会输出`nothing`。

* default_if_none

如果值是`None`，那么将会使用`default_if_none`提供的默认值。这个和`default`有区别，`default`是所有被评估为`False`的都会使用默认值。而`default_if_none`则只有这个值是等于`None`的时候才会使用默认值。示例代码如下：

```python
{{ value|default_if_none:"nothing" }}
```

如果`value`是等于`""`也即空字符串，那么以上会输出空字符串。如果`value`是一个`None`值，以上代码才会输出`nothing`。

* first

返回列表/元组/字符串中的第一个元素。示例代码如下：

```python
{{ value|first }}
```

如果`value`是等于`['a','b','c']`，那么输出将会是`a`。

* last

返回列表/元组/字符串中的最后一个元素。示例代码如下：

```python
{{ value|last }}
```

如果`value`是等于`['a','b','c']`，那么输出将会是`c`。

* floatformat

使用四舍五入的方式格式化一个浮点类型。如果这个过滤器没有传递任何参数。那么只会在小数点后保留一个小数，如果小数后面全是0，那么只会保留整数。当然也可以传递一个参数，标识具体要保留几个小数。

1. 如果没有传递参数：

   | value | 模版代码 | 输出 | | --- | --- | --- | | 34.23234 | `{{ value\|floatformat }}` | 34.2 | | 34.000 | `{{ value\|floatformat }}` | 34 | | 34.260 | `{{ value\|floatformat }}` | 34.3 |

2. 如果传递参数：

   | value | 模版代码 | 输出 | | --- | --- | --- | | 34.23234 | `{{value\|floatformat:3}}` | 34.232 | | 34.0000 | `{{value\|floatformat:3}}` | 34.000 | | 34.26000 | `{{value\|floatformat:3}}` | 34.260 |

* join

类似与`Python`中的`join`，将列表/元组/字符串用指定的字符进行拼接。示例代码如下：

```python
{{ value|join:"/" }}
```

如果`value`是等于`['a','b','c']`，那么以上代码将输出`a/b/c`。

* length

获取一个列表/元组/字符串/字典的长度。示例代码如下：

```python
{{ value|length }}
```

如果`value`是等于`['a','b','c']`，那么以上代码将输出`3`。如果`value`为`None`，那么以上将返回`0`。

* lower

将值中所有的字符全部转换成小写。示例代码如下：

```python
{{ value|lower }}
```

如果`value`是等于`Hello World`。那么以上代码将输出`hello world`。

* upper

类似于`lower`，只不过是将指定的字符串全部转换成大写。

* random

在被给的列表/字符串/元组中随机的选择一个值。示例代码如下：

```python
{{ value|random }}
```

如果`value`是等于`['a','b','c']`，那么以上代码会在列表中随机选择一个。

* safe

标记一个字符串是安全的。也即会关掉这个字符串的自动转义。示例代码如下：

```python
{{value|safe}}
```

如果`value`是一个不包含任何特殊字符的字符串，比如``这种，那么以上代码就会把字符串正常的输入。如果`value`是一串`html`代码，那么以上代码将会把这个`html`代码渲染到浏览器中。

* slice

类似于`Python`中的切片操作。示例代码如下：

```python
{{ some_list|slice:"2:" }}
```

以上代码将会给`some_list`从`2`开始做切片操作。

* stringtags

删除字符串中所有的`html`标签。示例代码如下：

```python
{{ value|striptags }}
```

如果`value`是`hello world`，那么以上代码将会输出`hello world`。

* truncatechars

如果给定的字符串长度超过了过滤器指定的长度。那么就会进行切割，并且会拼接三个点来作为省略号。示例代码如下：

```python
{{ value|truncatechars:5 }}
```

如果`value`是等于`北京欢迎您~`，那么输出的结果是`北京...`。可能你会想，为什么不会`北京欢迎您...`呢。因为三个点也占了三个字符，所以`北京`+三个点的字符长度就是5。

* truncatechars_html

类似于`truncatechars`，只不过是不会切割`html`标签。示例代码如下：

```python
{{ value|truncatechars:5 }}
```

如果`value`是等于`北京欢迎您~`，那么输出将是`北京...`。

### 自定义模版过滤器

* 模版过滤器必须要放在`app`中，并且这个`app`必须要在`INSTALLED_APPS`中进行安装
* 然后再在这个`app`下面创建一个`Python包`叫做`templatetags`
* 再在这个包下面创建一个存储过滤器的`python文件`
* 过滤器实际上就是python中的一个函数，只不过是把这个函数注册到模板库中，以后在模板中就可以使用这个函数了。但是这个函数的参数有限制，第一个参数必须是这个过滤器需要处理的值，第二个参数可有可无，如果有，那么就意味着在模板中可以传递参数。**并且过滤器的函数最多只能有两个参数**
* 以后想要在模板中使用这个过滤器，就要在模板中`load`一下这个过滤器所在的模块文件的名字（也就是这个存储python文件的名字）。

app2/templatetags/customize.py

~~~python
from django import template

register = template.Library()

'''
过滤器最多能有两个参数
过滤器的第一个参数永远都是被过滤的那个参数，也就是竖线左边的参数

过滤器的注册方式一：
使用 register.filter() 将函数注册到 template 库中 成为一个模板过滤器
register.filter() 中的第一个参数是过滤器的名字，第二个参数是对应的要注册的函数名

过滤器的注册方式二：
使用装饰器 @register.filter 将函数注册到 template 库中 成为一个模板过滤器
@register.filter 默认会将函数的名字作为过滤器的名字进行注册，如果想要自定义过滤器的名字就想过滤器传递一个名字的字符串参数就可以了
'''


# 过滤器的注册方式一
def new_word(value1, value2):
    return value1 + value2


register.filter("str_joint", new_word)


# 过滤器的注册方式二 自定义过滤器的名称为 list_joint
@register.filter("list_joint")
def new_list(value1, value2):
    return [value1, value2]


# 过滤器的注册方式二 默认过滤器的名称为函数名称 hello
@register.filter
def hello(value1, value2=None):
    if value2:
        return value2 + value1
    else:
        return 'Hello ' + value1

~~~

app2/views.py

~~~python
# ------------------------ 自定义模版过滤器 ------------------------

def template12(request):
    context = {
        'v1': 'ku_',
        'v2': 'rong',
        'v3': 'Django',
        'v4': 'Flask',
        'v5': 'Rong',
        'v6': 'ku_rong'
    }
    return render(request, 'app2/app2-12自定义模版过滤器.html', context=context)
~~~

app2/urls.py

~~~python
from django.urls import path

from app2 import views

app_name = 'app2'

urlpatterns = [
  	...	
    # 自定义模版过滤器
    path('template12/', views.template12, name='app2-12'),
]

~~~

templates/app2/app2-12自定义模版过滤器.html

~~~html
{% load customize %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>自定义模版过滤器</title>
</head>
<body>
    <h1>自定义模版过滤器</h1>
    <h2>Name: {{ v1|str_joint:v2 }}</h2>
    <h2>Like: {{ v3|list_joint:v4 }}</h2>
    <h2>{{ v5|hello }}</h2>
    <h2>{{ v6|hello:'最帅的小哥哥是：' }}</h2>
</body>
</html>
~~~

### 模版优化-引入模版

有时候一些代码是在许多模版中都用到的。如果我们每次都重复的去拷贝代码那肯定不符合项目的规范。一般我们可以把这些重复性的代码抽取出来，就类似于Python中的函数一样，以后想要使用这些代码的时候，就通过`include`包含进来。这个标签就是`include`

`include`标签寻找路径的方式。也是跟`render`渲染模板的函数是一样的。

默认`include`标签包含模版，会自动的使用主模版中的上下文，也即可以自动的使用主模版中的变量。如果想传入一些其他的参数，那么可以使用`with`语句。

app2/views.py

~~~python
# ------------------------ 模版优化-引入模版 ------------------------
def template13(request):
    context = {'username': 'ku_rong'}
    return render(request, 'app2/app2-13模版优化-引入模版.html', context=context)
~~~

app2/urls.py

~~~python
from django.urls import path

from app2 import views

app_name = 'app2'

urlpatterns = [
  	...
    # 模版优化-引入模版
    path('template13/', views.template13, name='app2-13'),
]
~~~

templates/app2/app2-13模版优化-引入模版.html

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>模版优化-引入模版</title>
</head>
<body>
{% include 'app2/app2-13模版优化-引入模版01.html' %}
<div class="content"><h1>模版优化-引入模版</h1></div>
{% if age %}
    {% include 'app2/app2-13模版优化-引入模版03.html' %}
{% else %}
    {% include 'app2/app2-13模版优化-引入模版03.html' with age=18 %}
{% endif %}

{% include 'app2/app2-13模版优化-引入模版02.html' %}

</body>
</html>
~~~

templates/app2/app2-13模版优化-引入模版01.html

~~~html
<header>
    <h1>This is include header</h1>
</header>
~~~

templates/app2/app2-13模版优化-引入模版02.html

~~~html
<footer>
    <h1>This is include foot</h1>
</footer>
~~~

templates/app2/app2-13模版优化-引入模版03.html

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>Hello {{ username }}, This is include username</h1>
    <h1>Age: {{ age }}</h1>
</body>
</html>
~~~

### 模版优化-模版继承

模版继承类似于`Python`中的类，在父类中可以先定义好一些变量和方法，然后在子类中实现。模版继承也可以在父模版中先定义好一些子模版需要用到的代码，然后子模版直接继承就可以了。并且因为子模版肯定有自己的不同代码，因此可以在父模版中定义一个block接口，然后子模版再去实现。

⚠️*注意* extends标签必须放在模版的第一行，子模板中的代码必须放在block中，否则将不会被渲染。

* 如果在某个`block`中需要使用父模版的内容，那么可以使用`{{block.super}}`来继承。
* 在定义`block`的时候，除了在`block`开始的地方定义这个`block`的名字，还可以在`block`结束的时候定义名字。比如`{% block title %}{% endblock title %}`。这在大型模版中显得尤其有用，能让你快速的看到`block`包含在哪里。

app2/views.py

~~~python
# ------------------------ 模版优化-模版继承 ------------------------
def template14(request):
    context = {'username': 'ku_rong', 'age': 18}
    return render(request, 'app2/app2-14模版优化-模版继承.html', context=context)
~~~

app2/urls.py

~~~python
from django.urls import path

from app2 import views

app_name = 'app2'

urlpatterns = [
  	...
  	# 模版优化-模版继承
    path('template14/', views.template14, name='app2-14')

]
~~~

templates/app2/app2/app2-14模版优化-模版继承base.html

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>模版优化-模版继承</title>
</head>
<body>
    <header>
        <h1>This is base header</h1>
    </header>
    {% block content %}
    Hello {{ username }}! I am base html
    {% endblock %}
    <footer>
        <h1>This is base footer</h1>
    </footer>
</body>
</html>
~~~

templates/app2/app2/app2-14模版优化-模版继承.html

~~~html
{% extends 'app2/app2-14模版优化-模版继承base.html' %}

{% block content %}
    <h1>{{ block.super }}</h1>
    <h1>{{ username }}'s Age is {{ age }}</h1>
{% endblock %}
~~~

### 模版中加载静态文件

在`DTL`中，使用`static`标签来加载静态文件。要使用`static`标签，首先需要`{% load static %}`。加载静态文件的步骤如下

1. 首先确保`django.contrib.staticfiles`已经添加到`settings.INSTALLED_APPS`中

2. 确保在`settings.py`中设置了`STATIC_URL`

3. 在已经安装了的`app`下创建一个文件夹叫做`static`，然后再在这个`static`文件夹下创建一个当前`app`的名字的文件夹，再把静态文件放到这个文件夹下。例如你的`app`叫做`book`，有一个静态文件叫做`zhiliao.jpg`，那么路径为`book/static/book/zhiliao.jpg`。（为什么在`app`下创建一个`static`文件夹，还需要在这个`static`下创建一个同`app`名字的文件夹呢？原因是如果直接把静态文件放在`static`文件夹下，那么在模版加载静态文件的时候就是使用`zhiliao.jpg`，如果在多个`app`之间有同名的静态文件，这时候可能就会产生混淆。而在`static`文件夹下加了一个同名`app`文件夹，在模版中加载的时候就是使用`app/zhiliao.jpg`，这样就可以避免产生混淆。）

4. 如果有一些静态文件是不和任何`app`挂钩的。那么可以在`settings.py`中添加`STATICFILES_DIRS`，以后`DTL`就会在这个列表的路径中查找静态文件。比如可以设置为:

   ~~~python
   STATICFILES_DIRS = [
        os.path.join(BASE_DIR,"static")
    ]
   ~~~

5. 在模版中使用`load`标签加载`static`标签。比如要加载在项目的`static`文件夹下的`style.css`的文件。

6. 如果不想每次在模版中加载静态文件都使用`load`加载`static`标签，那么可以在`settings.py`中的`TEMPLATES/OPTIONS`添加`'builtins':['django.templatetags.static']`，这样以后在模版中就可以直接使用`static`标签，而不用手动的`load`了。

7. 如果没有在`settings.INSTALLED_APPS`中添加`django.contrib.staticfiles`。那么我们就需要手动的将请求静态文件的`url`与静态文件的路径进行映射了。示例代码如下：

   ~~~python
   from django.conf import settings
   from django.conf.urls.static import static
   
   urlpatterns = [
       # 其他的url映射
   ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   ~~~

   

app2/views.py

~~~python
# ------------------------ 加载静态文件 ------------------------
def template15(request):
    context = {}
    return render(request, 'app2/app2-15加载静态文件.html', context=context)


def template16(request):
    context = {}
    return render(request, 'app2/app2-15加载静态文件static内置.html', context=context)
~~~

app2/urls.py

~~~python
from django.urls import path

from app2 import views

app_name = 'app2'

urlpatterns = [
  	...
    # 加载静态文件
    path('template15/', views.template15, name='app2-15'),
    path('template16/', views.template16, name='app2-16'),

]
~~~

templates/app2/app2-15加载静态文件.html

~~~html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>加载静态文件</title>
</head>
<body>
<h1>加载app2/static/app2/Django.png</h1>
<img src="{% static 'app2/Django.png' %}" alt="">
<h1>加载/static/app2/Python.png</h1>
<img src="{% static 'app2/Python.png' %}" alt="">
<h1>加载/static/world.jpeg</h1>
<img src="{% static 'world.jpeg' %}" alt="">
</body>
</html>
~~~

templates/app2/app2-15加载静态文件static内置.html

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>static 变成内置标签，不用load</title>
</head>
<body>
<h1>加载app2/static/app2/Django.png</h1>
<img src="{% static 'app2/Django.png' %}" alt="">
<h1>加载/static/app2/Python.png</h1>
<img src="{% static 'app2/Python.png' %}" alt="">
<h1>加载/static/world.jpeg</h1>
<img src="{% static 'world.jpeg' %}" alt="">
</body>
</html>
~~~

settings.py

~~~python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app1',
    'app2',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # django模版的查找路径
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # 设置为True表示django除了去DIRS里面的路径查找模版文件，还会去app下面查找templates(app必须在INSTALLED_APPS中注册)
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 将模版标签添加到 builtins 中，变成django的内置标签，以后在模版中使用的时候就不用load
            'builtins': [
                # 将static添加到builtins中，将static变成django内置标签
                'django.templatetags.static'
            ]
        },
    },
]

# STATIC_URL 是用来在浏览其中请求静态文件的URL 如127.0.0.1/static/xxx.jpng
STATIC_URL = '/static/'
# 不和任何 app 相关的静态文件，或者其它特殊的静态文件都可以放到 STATICFILES_DIRS 中添加的目录中单独区别存放
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
~~~
