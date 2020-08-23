from django.http import HttpResponse


def app1_inclued(request):
    return HttpResponse('<h1>This is Include path</h1>')
