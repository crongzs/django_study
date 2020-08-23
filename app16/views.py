from django.shortcuts import render
from django.http import HttpResponse

from app16.models import App16Artivle
from app16.utils.mtoh import ToHtml


# Create your views here.


def article_list(request):
    articles = App16Artivle.objects.first()
    content = ToHtml(articles.content).to_html()
    context = {
        'title': articles.title,
        'content': content,
        'created': articles.ts_created
    }

    return render(request, 'app16/app16-1list.html', context=context)
