from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.db.models import F

from app11.forms import APP11Form1, APP11Form2, APP11Form3
from app11.models import App11User
from app11.descorators import login_required  # 自定义的一个验证是否登陆的装饰器
from django.utils.decorators import method_decorator


# Create your views here.

@method_decorator(login_required, name='dispatch')
class IndexView(View):

    def get(self, request):
        return HttpResponse('Welcome ICBC')


class LoginView(View):

    def get(self, request):
        return render(request, 'app11/app11-1login.html')

    def post(self, request):
        form = APP11Form2(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            pwd = form.cleaned_data.get('pwd')
            user = App11User.objects.filter(name=name, pwd=pwd).first()
            if user:
                request.session['user_id'] = user.pk
                return redirect('app11:app11-1')
            else:
                return render(request, 'app11/app11-1login.html')
        else:
            return render(request, 'app11/app11-1login.html')


class RegisterView(View):

    def get(self, request):
        return render(request, 'app11/app11-2register.html')

    def post(self, request):
        form = APP11Form1(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            pwd = form.cleaned_data.get('pwd')
            phone = form.cleaned_data.get('phone')
            user = App11User.objects.create(name=name, pwd=pwd, phone=phone, balance=1000)
            user.save()
            return redirect('app11:app11-2')
        else:
            return render(request, 'app11/app11-2register.html')


@method_decorator(login_required, name='dispatch')
class TransferView(View):

    def get(self, request):
        return render(request, 'app11/app11-3transfer.html')

    def post(self, request):
        form = APP11Form3(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            money = form.cleaned_data.get('money')
            # user_id = request.session.get('user_id')
            # user = App11User.objects.get(pk=user_id)
            user = request.app11_user

            if user.balance >= money:
                user.balance -= money
                App11User.objects.filter(phone=phone).update(balance=F('balance') + money)
                user.save()
                return HttpResponse('successful')
            else:
                return HttpResponse('fail')
        else:
            return render(request, 'app11/app11-3transfer.html')


class LogOutView(View):
    def get(self, request):
        request.session.flush()
        return redirect('app11:app11-1')


class VirusView(View):
    ''' 模拟病毒网站 '''

    def get(self, request):
        ''' 实现csrf攻击 '''
        return render(request, 'app11/app11-4csrf攻击.html')
