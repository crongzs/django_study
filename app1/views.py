from django.shortcuts import render, redirect, reverse

# Create your views here.


from django.http import HttpResponse


def index_django_study(request):
    return HttpResponse('<h1>Hello, This is Django Study Index</h1>')


def index(request):
    return HttpResponse('<h1>Hello, This is App1 URL与视图 Index</h1>')


# ------------------- URL中传递参数给视图函数 -------------------

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


# ------------------- 实例命名空间 -------------------


def url_args6(request):
    username = request.GET.get('username')
    if username:
        return HttpResponse('<h1>This isi URL6, username is {}</h1>'.format(username))
    else:
        current_namespace = request.resolver_match.namespace  # 获取当前实例名称
        return redirect(reverse('%s:args-7' % current_namespace))


def url_args7(request):
    return HttpResponse('<h1>This is URL7</h1>')


def url_args8(request, year, month):
    ''' re_path 的使用'''
    return HttpResponse('<h1>This is URL8 {}-{}</h1>'.format(year, month))


# ------------------- URL带参数反转 -------------------


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
    return redirect(reverse('app1-a:args-12') + '?next={}'.format(app_name))


def url_args12(request):
    next = request.GET.get('next')
    return HttpResponse('<h1>This is URL12 next view is {}</h1>'.format(next))


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


# ------------------- URL映射指定默认参数 -------------------

def url_args15(request, page=1):
    ''' 在视图函数中指定默认参数 '''
    return HttpResponse('<h1>This is URL15 Page is {} </h1>'.format(page))


def url_args16(request):
    return HttpResponse('<h1>This is URL16</h1>')


def url_args(request):
    return HttpResponse('<h1>This is URL</h1>')
