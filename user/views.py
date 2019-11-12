from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, HttpResponse, reverse, redirect
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSS, SignatureExpired
from django.views.generic import View, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from olens import settings
from .forms import RegisterForm, LoginForm
from .models import User
from celery_task.tasks import send_signup_active_mail

# Create your views here.

# https://segmentfault.com/a/1190000009455783?utm_source=tag-newest
# https://juejin.im/post/5c9756296fb9a070ad504a05
# https://code.ziqiangxuetang.com/django/django-generic-views.html




class Singup(View):
    '''注册'''

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
            user.is_active = 0  # 设置激活状态
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
    '''登录'''

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):

        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)  # 登录

            return redirect(reverse('home'))
        else:
            return render(request, 'login.html', {'form': form})


# https://www.jianshu.com/p/af04705b5245
# @login_required() 注意 这里不能直接装饰
@method_decorator(login_required, name='dispatch')
class UserCenter(ListView):

    model = User
    # templates_name = 'homepage.html'
    template_name = 'homepage.html'
    context_object_name = 'users'



def active(request, token):
    ''' 激活 '''

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

def signout(request):

    if request.method == 'GET':

        logout(request)  # 退出登录  清除session

        # 跳转到首页
        return redirect(reverse('index'))











