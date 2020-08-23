from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

# Create your views here.

from app12.models import App12Comment

import bleach
from bleach.sanitizer import ALLOWED_ATTRIBUTES, ALLOWED_TAGS


def app12_1(request):
    context = {
        'comments': App12Comment.objects.all()
    }

    return render(request, '', context=context)


@require_http_methods(['POST'])
def app12_2(request):
    content = request.POST.get('context')
    tags = ALLOWED_TAGS + ['img']
    attributes = {**ALLOWED_ATTRIBUTES, 'img': ['src']}
    # cleaned_data = bleach.clean(content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
    cleaned_data = bleach.clean(content, tags=tags, attributes=attributes)
    App12Comment.objects.create(content=cleaned_data)
    return redirect('app12:app12-1')
