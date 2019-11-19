from django import forms
from django.forms import widgets
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm

class RegisterForm(forms.Form):

    name = forms.CharField(
        max_length = 12,
        min_length = 4,
        required = True,
        error_messages = {'required':'用户名不能为空', 'invalid':'格式不对'},
        widget = widgets.TextInput(attrs={'class':'form-control loon luser',
                                          'placeholder':'用户名'})
    )

    password = forms.CharField(
        required = True,
        max_length = 32,
        min_length = 6,
        error_messages = {'required': '密码不能为空', 'invalid':'密码格式不对'},
        widget = widgets.PasswordInput(attrs={'class':'form-control loon lpass',
                                              'placeholder': '密码在六位以上'})
    )

    password_confum = forms.CharField(
        required = True,
        max_length = 32,
        min_length = 6,
        error_messages = {'required': '密码不能为空', 'invalid':'密码格式不对'},
        widget = widgets.PasswordInput(attrs={'class': 'form-control loon lpass',
                                              'placeholder': '输入再次密码'})
    )

    email = forms.EmailField(
        widget = widgets.EmailInput(attrs={'class':' form-control loon lpass',
                                           'placeholder':'邮箱'})
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
                               required=True,
                               error_messages={'required':'用户名不能为空', 'invalid':'格式不对'},
                               widget=widgets.TextInput(attrs={'class':'form-control loon lpass',
                                                             'placeholder':'用户名'}))

    password = forms.CharField(max_length=32,
                               min_length=6,
                               required=True,
                               error_messages = {'required':'密码不能为空', 'invalid':'格式不对'},
                               widget=widgets.PasswordInput(attrs={'class':'form-control loon lpass',
                                                                    'placeholder': '密码在六位以上'}))

    def clean(self):

        cleaned_data = self.cleaned_data
        username = self.cleaned_data['username']
        pwd = self.cleaned_data['password']
        print(username, pwd)

        user = authenticate(username=username, password=pwd)
        print(user)
        if not user:
            raise forms.ValidationError('用户名或密码错误')
        if not user.is_active:
            raise forms.ValidationError('用户未激活')

        return cleaned_data


class MyChangePasswordFrom(PasswordChangeForm):

    # def __init__(self, user, *args, **kwargs):
    #     self.user = user
    #     super().__init__(*args, **kwargs)

    old_password = forms.CharField(max_length=32,
                                   min_length=6,
                                   required=True,
                                   error_messages={'required':'密码不能为空', 'invalid':'格式不对'},
                                   widget=widgets.PasswordInput(attrs={'class': 'form-control loon lpass',
                                                                        'placeholder': '密码在六位以上'}))

    new_password1 = forms.CharField(max_length=32,
                                    min_length=6,
                                    required=True,
                                    error_messages={'required': '密码不能为空', 'invalid': '格式不对'},
                                    widget=widgets.PasswordInput(attrs={'class': 'form-control loon lpass',
                                                                        'placeholder': '新密码'}))

    new_password2 = forms.CharField(max_length=32,
                                    min_length=6,
                                    required=True,
                                    error_messages={'required': '密码不能为空', 'invalid': '格式不对'},
                                    widget=widgets.PasswordInput(attrs={'class': 'form-control loon lpass',
                                                                        'placeholder': '确认密码,请在输入一次'}))

    # def clean_raw_password(self):
    #
    #     if not self.user.check_password():
    #
    #         raise forms.ValidationError('原密码输入错误')
    #     return self.raw_password

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError('原密码错误')
        return old_password



