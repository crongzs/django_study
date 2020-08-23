from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib import messages

# Create your views here.

from app10.models import APP10User


class IndexView(View):

    def get(self, request):

        user = request.app10_user
        if user:
            content = '<h1>Hello %s</h1>' % user.name
        else:
            content = 'Please log in before that'

        return HttpResponse(content)


class SiginView(View):

    def get(self, request):
        return render(request, 'app10/app10-1login.html')

    def post(self, request):
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        print('--------', name, '--------')
        print('--------', pwd, '--------')
        user = APP10User.objects.filter(name=name, pwd=pwd).first()
        if user:
            request.session['user_id'] = user.id
            return redirect('app10:app10-1')
        else:
            messages.info(request, '用户名或者密码错误')
            return render(request, 'app10/app10-1login.html')
