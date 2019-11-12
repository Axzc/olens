from django.urls import path, re_path
from user.views import Singup, Login, UserCenter
from user import views

urlpatterns = [
    path('signup', Singup.as_view(), name="signup" ),
    path('login', Login.as_view(), name='login'),
    path('usercenter', UserCenter.as_view(), name='usercenter'),
    path('logout', views.signout, name='logout'),
    re_path('active/(?P<token>.*)', views.active, name='active'),
]

