from app9.models import App9User


def login_user(request):
    user = request.session.get('user')
    context = {}
    if user:
        try:
            u = App9User.objects.get(pk=user)
            context['username'] = u.name
        except:
            pass

    return context
