from django.contrib import admin
from django.urls import path, include
from article import views
from article.views import IndexView
import user.urls

urlpatterns = [
  path('', IndexView.as_view(), name='index'),
  path('home', views.home, name='home')
]