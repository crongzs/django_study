from django.shortcuts import render
from django.views import View
# Create your views here.

from django.http import HttpResponse

# ---------------- Django 表单的使用流程 ----------------


from app5.forms import MessageBoardForm


class MessageVoarView(View):

    def get(self, request):
        form = MessageBoardForm()
        return render(request, 'app5/app5-1forms.html', context={'form': form})

    def post(self, request):
        form = MessageBoardForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            email = form.cleaned_data.get('email')
            reply = form.cleaned_data.get('reply')
            print(title)
            print('*' * 30)
            print(content)
            print('*' * 30)
            print(email)
            print('*' * 30)
            print(reply)
            return HttpResponse('successful')
        else:
            print(form.errors.get_json_data())
            return HttpResponse('fail')


# ---------------- 用表单验证数据是否合法 ----------------

from app5.forms import VerifyForm


class VerifyView(View):
    def get(self, request):
        return render(request, 'app5/app5-2verify.html')

    def post(self, request):
        form = VerifyForm(request.POST)
        if form.is_valid():
            return HttpResponse('suucessful')
        else:
            print('----------error----------')
            print(form.errors.get_json_data())
            return HttpResponse('fail')


# ---------------- 使用表单验证器 ----------------

from app5.forms import ValidactorsForm


class ValidactorView(View):
    def get(self, request):
        return render(request, 'app5/app5-3validators.html')

    def post(self, request):
        form = ValidactorsForm(request.POST)
        if form.is_valid():
            return HttpResponse('successful')
        else:
            print(form.errors.get_json_data())
            return HttpResponse('fail')


# ---------------- 自定义表单验证器 ----------------
from app5.forms import UserdefinedForm
from app5.models import FormUser


class UserdefinedView(View):
    def get(self, request):
        return render(request, 'app5/app5-4userdefined.html')

    def post(self, request):
        form = UserdefinedForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            phone = form.cleaned_data.get('phone')
            FormUser.objects.create(name=name, phone=phone)
            return HttpResponse('successful')
        else:
            print(form.errors.get_json_data())
            return HttpResponse('fail')


# ---------------- 简化错误信息提取 ----------------
from app5.forms import GetErrorsForm
from app5.models import FormUser


class GetErrorView(View):
    def get(self, request):
        return render(request, 'app5/app5-4userdefined.html')

    def post(self, request):
        form = GetErrorsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            phone = form.cleaned_data.get('phone')
            FormUser.objects.create(name=name, phone=phone)
            return HttpResponse('successful')
        else:
            errors = form.errors.get_json_data()
            error = list(errors.keys())[0] + ': ' + errors[list(errors.keys())[0]][0]['message']
            return HttpResponse(error)


# ---------------- ModelForm ----------------
from app5.forms import BookFrom


class BookView(View):
    def get(self, request):
        return HttpResponse('ModelForm')

    def post(self, request):
        form = BookFrom(request.POST)
        if form.is_valid():
            return HttpResponse('successful')
        else:
            print(form.errors.get_json_data())
            return HttpResponse('fail')


from django.views.decorators.http import require_http_methods, require_POST, require_GET
from app5.forms import User2Form


@require_POST
def add_user(request):
    ''' ModelForm 的 save() 方法 '''
    form = User2Form(request.POST)
    if form.is_valid():
        # 这样直接使用 save()方法 必须要保证表单中的fields字段列表中的数据满足 模型中的所有字段需求，也就是 __all__
        # form.save()
        # 如果 forms 中的 fields 不能满足 models 中的需求，那么就在save 方法中 添加参数 commit=False
        pwd = form.cleaned_data.get('pwd1')
        user = form.save(commit=False)
        user.password = pwd
        user.save()
        return HttpResponse('successful')
    else:
        print(form.errors.get_json_data())
        return HttpResponse('fail')
