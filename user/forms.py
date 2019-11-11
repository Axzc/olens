from django import forms
from django.forms import widgets
from .models import User

from django.contrib.auth import authenticate

class RegisterForm(forms.Form):

    name = forms.CharField(
        max_length = 12,
        min_length = 4,
        required = True,
        error_messages = {'required':'用户名不能为空', 'invalid':'格式不对'},
        # widget = widgets.TextInput()
        widget = widgets.TextInput(attrs={'class':'form-control loon luser', 'placeholder':'用户名'})
        # widget = widgets.TextInput(attrs={'class': 'form-control loon luser', 'value': '用户名'})
    )

    password = forms.CharField(
        required = True,
        max_length = 32,
        min_length = 6,
        error_messages = {'required': '密码不能为空', 'invalid':'密码格式不对'},
        widget = widgets.PasswordInput(attrs={'class':'form-control loon lpass', 'placeholder': '输入密码'})
    )

    password_confum = forms.CharField(
        required = True,
        max_length = 32,
        min_length = 6,
        error_messages = {'required': '密码不能为空', 'invalid':'密码格式不对'},
        widget = widgets.PasswordInput(attrs={'class':'form-control loon lpass', 'placeholder': '输入再次密码'})
    )

    email = forms.EmailField(
        widget = widgets.EmailInput(attrs={'class':'form-control loon lpass', 'placeholder':'邮箱'})
    )

    def clean(self):

        cleaned_data = self.cleaned_data
        username = self.cleaned_data['name']
        pwd = self.cleaned_data['password']
        re_pwd = self.cleaned_data['password_confum']
        email1 = self.cleaned_data['email']

        print('wai', pwd)
        print('re_pwd', re_pwd)

        if pwd != re_pwd:
            raise forms.ValidationError('两次输入的密码不匹配')

        user = User.objects.filter(username = username)
        if user:
            raise forms.ValidationError('这个用户名已经被注册了')

        em = User.objects.filter(email = email1)
        if em:
            raise forms.ValidationError('该邮箱已经注册了, 登录?')

        return cleaned_data


class LoginForm(forms.Form):

    username = forms.CharField(max_length=12,
                           min_length=4,
                           required = True,
                           error_messages = {'required':'用户名不能为空', 'invalid':'格式不对'},
                           widget = widgets.TextInput(attrs={'class':'form-control loon luser', 'placeholder':'用户名'}))

    password = forms.CharField(max_length=32,
                               min_length=6,
                               required=True,
                               error_messages = {'required':'密码不能为空', 'invalid':'格式不对'},
                               widget = widgets.PasswordInput(attrs={'class':'form-control loon lpass', 'placeholder': '输入密码'}))

    def clean(self):

        cleaned_data = self.cleaned_data
        username = self.cleaned_data['usernmae']
        pwd = self.cleaned_data['password']
        print(username, pwd)

        user = authenticate(username=username, password=pwd)
        print(user)
        if not user:
            raise forms.ValidationError('用户名或密码错误')
        if not user.is_active:
            raise forms.ValidationError('用户未激活')

        return cleaned_data






