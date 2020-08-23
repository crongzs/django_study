from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_POST, require_GET, require_safe

from app18.signals import self_signal1, self_signal2
from django.dispatch import Signal


# Create your views here.


def test_signal(request):
    self_signal1.send(sender=None, )
    print('This is a request test for self signal')
    return HttpResponse('<h1>Hello world</h1>')


@require_POST
def test_request_log(request):
    self_signal2.send(sender=None, request=request)
    return HttpResponse('<h1>Hello world</h1>')
