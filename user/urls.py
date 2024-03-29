from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from user.views import Singup, Login, UserCenter, ForgetPwdView, RestPasswordView
from user import views

urlpatterns = [
    path('signup', Singup.as_view(), name="signup"),
    path('login', Login.as_view(), name='login'),
    path('usercenter', UserCenter.as_view(), name='usercenter'),
    path('logout', views.signout, name='logout'),
    path('password-change', views.change_password, name= 'changepassword'),
    # path('password-change1', views.password_change1, name='password-change1'),
    re_path('active/(?P<token>.*)', views.active, name='active'),
    path('password-change-done', TemplateView.as_view(
        template_name='password_change_done.html'),
         name='pwdcd'),
    path('forgetpwd', ForgetPwdView.as_view(), name='forgetpwd'),
    re_path('resetpwd/(?P<token>.*)', RestPasswordView.as_view(), name="rsetpwd")
    # path('accounts/', include('django.contrib.auth.urls'))
]

# path('repwd', ChangePassword.as_view(), name='changepassword'),
# path('password-change/', auth_views.PasswordChangeView.as_view(
#     form_class=PasswordChangeForm,
#     template_name='password_change.html',
#     success_url=reverse_lazy('pwdcd')),name='changepassword1'),
