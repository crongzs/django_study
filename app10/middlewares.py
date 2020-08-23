from app10.models import APP10User


# 用函数定义的中间件
def app10_user_middleware(get_response):
    # 在执行中间件之前需要执行的一些初始化代码，放在外层函数中执行
    # 每次请求到达视图函数之前的一些代码，放在里面的函数里面执行
    print('这里执行的是 中间件初始化代码')
    print('请注意，这里的代码，只执行一次')

    def middleware(request):
        print('这里执行的是 request 到达 view 之前的代码')
        user_id = request.session.get('user_id')
        print('-----------', user_id, '-----------')
        if user_id:
            try:
                user = APP10User.objects.get(pk=user_id)
                request.app10_user = user
            except:
                pass
        # 在 response = get_response(request) 这个代码之前的代码，是request到view之前执行的代码
        # 在 response = get_response(request) 这个代码之后的代码，response到浏览器之前执行的代码
        response = get_response(request)
        print('这里执行的是 response 到达 浏览器 之前的代码')
        return response

    return middleware


# 用类定义的中间件
class App10UserMiddleware(object):

    def __init__(self, get_response):
        # 在执行中间件之前需要执行的一些初始化代码，放在构造函数中
        print('这里执行的是 中间件初始化代码')

        self.get_response = get_response

    def __call__(self, request):
        print('这里执行的是 request 到达 view 之前的代码')
        user_id = request.session.get('user_id')
        print('-----------', user_id, '-----------')
        if user_id:
            try:
                user = APP10User.objects.get(pk=user_id)
                request.app10_user = user
            except:
                pass
        # 在 response = get_response(request) 这个代码之前的代码，是request到view之前执行的代码
        # 在 response = get_response(request) 这个代码之后的代码，response到浏览器之前执行的代码
        response = self.get_response(request)
        print('这里执行的是 response 到达 浏览器 之前的代码')
        return response


# 将要被遗弃的中间件写法, 不推荐使用
from django.utils.deprecation import MiddlewareMixin


class App10UserMiddlewareMixin(MiddlewareMixin):

    def __init__(self, get_response):
        # 执行一些初始化的代码
        print('这里执行的是 中间件初始化代码')
        super(App10UserMiddlewareMixin, self).__init__(get_response)

    # 这个方法是 request 到达 view 之前调用的
    def process_request(self, request):
        print('这里是request到达view之前执行的代码')
        user_id = request.session.get('user_id')
        print('-----------', user_id, '-----------')
        if user_id:
            try:
                user = APP10User.objects.get(pk=user_id)
                request.app10_user = user
            except:
                request.app10_user = None
        else:
            request.app10_user = None

    # 这个方法是 response 到达浏览器之前执行的方法
    def process_response(self, request, response):
        print('这里执行的是 response 到达 浏览器 之前的代码')
        return response
