from django.contrib.auth import login
from django.shortcuts import render, HttpResponse, reverse, redirect
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSS, SignatureExpired
from django.views.generic import View
from olens import settings
from .forms import RegisterForm, LoginForm
from .models import User
from celery_task.tasks import send_signup_active_mail

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
            username = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')

            user = User.objects.create_user(username=username,
                                            password=password,
                                            email=email)
            user.is_active = 0
            user.save()
            print(username, password, email)

            # 加密
            tjwss = TJWSS(settings.SECRET_KEY, 900)
            info = {'confirm': user.id}
            token = tjwss.dumps(info).decode()


            # 发送邮件
            send_signup_active_mail.delay(email, username, token)


            return redirect(reverse('index'))
            # return HttpResponse('nice')
        else:
            return render(request, 'signup.html', {'form':form})


class Login(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):

        form = LoginForm(request.POST)

        if form.is_valid:

            login(form.cleaned_data['usernmae'], form.cleaned_data['password'])

            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {'form':form})



def active(request, token):

    if request.method == 'GET':
        tjwss = TJWSS(settings.SECRET_KEY, 900)

        try:
            # 获取解密信息
            info = tjwss.loads(token)
            user_id = info['confirm']
            user = User.objects.get(id = user_id)
            user.is_active = 1  # 修改激活状态
            user.save()

            return redirect(reverse('login'))


        except SignatureExpired as e:
            # 激活链接过期

            return HttpResponse('链接已过期')









