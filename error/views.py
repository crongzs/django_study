from django.shortcuts import render


def error_403(request):
    return render(request, 'error/403.html')


def error_405(request):
    return render(request, 'error/405.html')
