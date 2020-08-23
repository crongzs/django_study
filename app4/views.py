from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


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


# --------------------- HttpResponse 对象 ---------------------


def httpresponse(request):
    ''' HttpResponse 将要返回给浏览器的数据现包装一下再返回 '''

    # content_type 返回数据的MIME类型，默认为 text/html
    response = HttpResponse(
        content_type='text/plain;charset=utf-8')  # 将 content_type 设置为 text/plain 纯文本的类型, 并指定编码格式为utf-8
    # content 返回内容
    response.content = '<h1>Hello Django</h1>'
    # status_code 返回 http的状态吗，正常为200
    response.status_code = 200

    # 设置请求头
    response['passward'] = '960308'

    return response


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


from django.http import StreamingHttpResponse


def csv3(request):
    ''' 生成大的csv文件 '''

    response = StreamingHttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment;filename=large.csv"
    # response.streaming_content = ("username,age\n", "ku_rong,18\n")
    # 如果圆括号中使用for in 循环，那么它就会成为一个生成器
    row = ("Row {}.{}\n".format(row, row) for row in range(1, 100000))
    response.streaming_content = row

    return response


# --------------------- TemplateView ---------------------
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


# @method_decorator(['info_user', ...], name='dispatch') 如果有多个装饰器，还可以传递一个列表
@method_decorator(info_user, name='dispatch')  # 第二种装饰方法
class ArticlesView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('<hq>在 dispatch 上添加装饰器</h1>')

    # 第一种装饰方法
    # django 之中，如果要装饰一个方法的话，Django 提供了一个 装饰器 method_decorator 可以使装饰方法变得安全
    @method_decorator(info_user)
    def dispatch(self, request, *args, **kwargs):
        return super(ArticlesView, self).dispatch(request, *args, **kwargs)
