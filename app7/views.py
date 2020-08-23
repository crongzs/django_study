from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse
from django.core.cache import cache


def memcached1(request):
    cache.set("username", "ku_rong", 120)  # key value timeout
    username = cache.get("username")
    return HttpResponse("username: %s" % username)
