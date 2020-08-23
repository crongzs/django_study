from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib import messages

from app9.forms import App9From1, App9Form2
from app9.models import App9User


# Create your views here.


def app9_1(request):
    context = {}
    # user_id = request.session.get('user')
    # user = App9User.objects.get(pk=user_id)
    # context['username'] = user.name

    user = App9User.objects.all()
    if user:
        # 消息
        # 添加消息的第一种方式
        messages.add_message(request, messages.INFO, 'Hello i am a message!')  # 第一个参数是request，第二个是消息的级别，第三个是消息内容
        # 添加消息的第二种方式
        messages.info(request, "hello i'm a new message")  # 这种方式就免了消息级别的手动添加
    return render(request, 'app9/app9-1用户系统案例1.html', context=context)


# app9-1用户系统案例1

def app9_2(request):
    if request.method == 'GET':
        return render(request, 'app9/app9-4一部分Django默认上下文处理器.html')
    else:
        # 消息
        # 添加消息的第一种方式
        messages.add_message(request, messages.INFO, 'Hello i am a message!')  # 第一个参数是request，第二个是消息的级别，第三个是消息内容
        # 添加消息的第二种方式
        messages.info(request, "hello i'm a new message")  # 这种方式就免了消息级别的手动添加
        return render(request, 'app9/app9-4一部分Django默认上下文处理器.html')


class App9View1(View):

    def get(self, request):
        return render(request, 'app9/app9-2用户系统案例2.html')

    def post(self, request):
        form = App9From1(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app9:app9-1')
        else:
            return render(request, 'app9/app9-2用户系统案例2.html', {'message': 'register failed!'})


class App9View2(View):
    def get(self, request):
        return render(request, 'app9/app9-3用户系统案例3.html')

    def post(self, request):
        form = App9Form2(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            pwd = form.cleaned_data.get('pwd')
            user = App9User.objects.filter(name=name, pwd=pwd).first()
            if user:
                request.session['user'] = user.id
                return redirect('app9:app9-1')
            else:
                return redirect('app9:app9-3')
        else:
            return redirect('app9:app9-3')
