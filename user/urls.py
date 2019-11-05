from django.urls import path
from user.views import Singup

urlpatterns = [
    path('', Singup.as_view() , name="index" )
]

