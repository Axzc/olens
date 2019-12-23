from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, HttpResponse, reverse, redirect
from django.views.generic import View, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSS, SignatureExpired
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


from olens import settings
from .forms import RegisterForm, LoginForm, MyChangePasswordFrom, ForgetPasswordFrom, ResetPasswordFrom
from .models import User
from celery_task.tasks import send_signup_active_mail, send_forget_password_mail


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
            print(form.non_field_errors)
            return render(request, 'login.html', {'form': form})


# https://www.jianshu.com/p/af04705b5245
# @login_required() 注意 这里不能直接装饰
@method_decorator(login_required, name='dispatch')
class UserCenter(ListView):

    model = User
    template_name = 'homepage.html'
    context_object_name = 'users'

@login_required()
def change_password(request):

    '''修改密码 '''

    if request.method == 'GET':

        form = MyChangePasswordFrom(user=request.user)
        return render(request, 'password_change.html', {'form': form})

    if request.method == 'POST':

        user = request.user
        form = MyChangePasswordFrom(user=user, data=request.POST)
        print(form.is_valid(), "mylove")

        if form.is_valid():
            print("done")
            # form.save()  # 修改密码
            password = form.cleaned_data["new_password1"]
            user.set_password(password)  # 修改密码
            user.save()  # 提交

            return redirect(reverse('pwdcd'))
        else:
            print(form.non_field_errors,  "VIEWS")
            return render(request, 'password_change.html', {'form': form})


def active(request, token):
    ''' 激活 '''

    if request.method == 'GET':
        tjwss = TJWSS(settings.SECRET_KEY, 900)

        try:
            # 获取解密信息
            info = tjwss.loads(token)
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = 1  # 修改激活状态
            user.save()

            return redirect(reverse('login'))

        except SignatureExpired as e:
            # 激活链接过期
            # username = token_confirm.remove_validate_token(token)

            # user = User.objects.get(id=user_id)
            request.user.delete()
            return HttpResponse('链接已过期')


@login_required
def signout(request):

    if request.method == 'GET':

        logout(request)  # 退出登录  清除session

        # 跳转到首页
        return redirect(reverse('index'))

# def password_change1(request):
#
#     raw_pwd = request.get('raw-pwd')
#     print(raw_pwd)


class ForgetPwdView(View):
    """忘记密码"""

    def get(self, request):

        form = ForgetPasswordFrom()
        return render(request, 'forget_pwd.html', {'form': form})

    def post(self, request):
        form = ForgetPasswordFrom(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            tjwss = TJWSS(settings.SECRET_KEY, 900)
            info = {'confirm': user.id}
            token = tjwss.dumps(info).decode()
            send_forget_password_mail.delay(email, user.username, token)

            return HttpResponse("发送成功")
        else:
            return render(request, 'forget_pwd.html', {'form': form})


# FIXME
class RestPasswordView(View):
    """重置密码"""

    def get(self, request, token):
        form = ResetPasswordFrom()
        tjwss = TJWSS(settings.SECRET_KEY, 900)
        print(token)
        try:
            # 获取解密信息
            info = tjwss.loads(token)
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            request.user = user
            print(request.user, "&&&&&&&&&&&&&&&&&&&&&&get")
            return render(request, 'reset_pwd.html', {'form': form})

        except SignatureExpired as e:
            return HttpResponse('链接已过期')

    def post(self, request, token):

        form = ResetPasswordFrom(request.POST)
        print(request.user)
        if form.is_valid():
            password = form.cleaned_data['rest_new_password1']
            print(request.user, "************")
            request.user.set_password(password)
            return redirect(reverse('login'))
        else:
            return render(request, 'reset_pwd', {'form': form})


class CustomBackend(ModelBackend):
    """邮箱登录"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
















