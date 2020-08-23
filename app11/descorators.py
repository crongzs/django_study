from django.shortcuts import redirect
from app11.models import App11User


def login_required(func):
    def wrapper(request, *args, **kwargs):
        '''
        以下获取user的功能已经在中间件实现，不需要再重复查询

        user_id = request.session.get('user_id')
        exists = App11User.objects.filter(pk=user_id).exists()
        if exists:

        '''

        if request.app11_user:
            return func(request, *args, **kwargs)
        else:
            return redirect('app11:app11-2')

    return wrapper
