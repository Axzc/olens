from django.urls import path
from user.views import Singup

urlpatterns = [
    path('signup', Singup.as_view(), name="signup" )
]

