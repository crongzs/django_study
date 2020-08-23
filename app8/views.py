from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.utils.timezone import make_aware

from datetime import datetime


def cookie1(request):
    ''' 设置cookie '''
    response = HttpResponse('cookie')
    # response.set_cookie("username", "ku_rong", max_age=120)  # max_age 过期时间，如果不设置，会默认浏览器关闭后过期

    expires = datetime(year=2020, month=3, day=5, hour=20, minute=0, second=0)
    expires = make_aware(expires)
    # 如果 expires 和 max_age 都设置了，那么会以 expires 为主
    response.set_cookie("username", "ku_rong", expires=expires, max_age=120, path='/app8/cookie2/')  # path 指定有效路径

    return response


def cookie2(request):
    ''' 获取cookie '''
    cookies = request.COOKIES
    username = cookies.get('username')
    return HttpResponse('username: %s' % username)


def cookie3(request):
    ''' 删除cookie '''
    response = HttpResponse('delete cookie')
    response.delete_cookie('username')
    return response


def session1(request):
    ''' 添加session '''
    request.session['username'] = 'ku_rong'
    return HttpResponse('session')


def session2(request):
    ''' 获取session '''
    username = request.session.get('username')
    return HttpResponse('session, %s' % username)


def session3(request):
    ''' 删除session '''
    username = request.session.pop('username')
    return HttpResponse('session, %s' % username)


def session(request):
    return HttpResponse('session')


def cookie4(request):
    context = {
        'username': 'Rong'
    }

    response = render(request, 'app8/index.html', context)
    request.session['username'] = 'ku_rong'

