from django.shortcuts import render, reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from datetime import datetime


# Create your views here.


def template1(request):
    ''' render_to_string 渲染模版 '''
    html = render_to_string('app2-1.html')
    return HttpResponse(html)


def template2(request):
    ''' render 渲染模版'''
    return render(request, 'app2-1.html')


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


# ------------------------ for标签 ------------------------


def template5(request):
    context = {
        'persons': ['ku_rong', 'ronggege']
    }
    return render(request, 'app2/app2-5with标签.html', context=context)


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


# ------------------------ autoescape标签 ------------------------

def template9(request):
    context = {
        'url': "<p><a href='https://www.baidu.com/'>百度</a></p>"
    }
    return render(request, 'app2/app2-9autoescape标签.html', context=context)


# ------------------------ verbatim标签 ------------------------

def template10(request):
    context = {
        'hello': 'ku_rong'
    }
    return render(request, 'app2/app2-10verbatim标签.html', context=context)


# ------------------------ 常见的模版过滤器 ------------------------


def template11(request):
    context = {
        'v1': ['apple', 'banana'],
        'v2': ['chestnut', 'coconut'],
        'v3': 'apricot almond ...',
        'v4': '',
        'v5': None,
        'v6': ['blackberry', 'blueberry'],
        'v7': [30.260, 30.3222, 30.00],
        'v8': ['Banana', 'Bitter orange'],
        'v9': "<script>alert('Apricot');</script>",
        'v10': '<p>apricot almond</p>',
        'v11': 'apple apricot almond banana berry blackberry blueberry Bitter orange',
        'v12': '<p>apple apricot almond banana berry blackberry blueberry Bitter orange</p>',
        'now': datetime.now(),
    }
    return render(request, 'app2/app2-11常见的过滤器.html', context=context)


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


# ------------------------ 模版优化-引入模版 ------------------------
def template13(request):
    context = {'username': 'ku_rong'}
    return render(request, 'app2/app2-13模版优化-引入模版.html', context=context)


# ------------------------ 模版优化-模版继承 ------------------------
def template14(request):
    context = {'username': 'ku_rong', 'age': 18}
    return render(request, 'app2/app2-14模版优化-模版继承.html', context=context)


# ------------------------ 加载静态文件 ------------------------
def template15(request):
    context = {}
    return render(request, 'app2/app2-15加载静态文件.html', context=context)


def template16(request):
    context = {}
    return render(request, 'app2/app2-15加载静态文件static内置.html', context=context)


class Persion(object):
    def __init__(self, username):
        self.name = username
