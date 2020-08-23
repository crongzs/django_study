from django.shortcuts import render
from django.views import View
from django.http.response import JsonResponse

# Create your views here.

import logging

logger = logging.getLogger("django.request")


class UserView(View):

    def get(self, request):
        context = {
            'username': request.GET.get('username', ''),
            'age': request.GET.get('age', ''),
            'phone': request.GET.get('phone', '')
        }

        return JsonResponse(context)

    def post(self, request):

        context = {
            'username': request.POST.get('username', ''),
            'age': request.POST.get('age', ''),
            'phone': request.POST.get('phone', '')
        }

        logging.info('hello world')

        for x in ['username', 'age', 'phone']:
            if not context[x]:
                return JsonResponse({'message': '缺少必填项'})
        return JsonResponse(context)
