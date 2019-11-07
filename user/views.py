from django.shortcuts import render, HttpResponse
from django.views.generic import View
from .forms import RegisterForm

# Create your views here.

# https://segmentfault.com/a/1190000009455783?utm_source=tag-newest
# https://juejin.im/post/5c9756296fb9a070ad504a05
# https://code.ziqiangxuetang.com/django/django-generic-views.html




class Singup(View):

    def get(self, request):

        form = RegisterForm()

        return render(request, 'signup.html', {'form':form})

    def post(self, request):

        form = RegisterForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data.get('name'))
            print(form.cleaned_data.get('password'))

            return HttpResponse('nice')
        else:
            return render(request, 'signup.html', {'form':form})




