from django.urls import path, re_path
from user.views import Singup, Login
from user import views

urlpatterns = [
    path('signup', Singup.as_view(), name="signup" ),
    path('login', Login.as_view(), name='login'),
    re_path('active/(?P<token>.*)', views.active, name='active'),
]

