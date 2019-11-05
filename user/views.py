from django.shortcuts import render, HttpResponse
from django.views.generic import View

# Create your views here.

# https://segmentfault.com/a/1190000009455783?utm_source=tag-newest
# https://juejin.im/post/5c9756296fb9a070ad504a05
# https://code.ziqiangxuetang.com/django/django-generic-views.html




class Singup(View):

    def get(self, request):

        return HttpResponse("1")

    def post(self, request):

        pass


