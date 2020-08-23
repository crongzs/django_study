from app11.models import App11User


def app11_user_middleware(get_response):
    print("app11 初始化")

    def middleware(request):
        print("request到达view之前执行的代码")
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = App11User.objects.get(pk=user_id)
                request.app11_user = user
            except:
                request.app11_user = None
        else:
            request.app11_user = None
        response = get_response(request)
        print("response到达浏览器之前执行的代码")
        return response

    return middleware
