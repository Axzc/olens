from django.contrib import admin
from django.urls import path, include
from article import views
import user.urls

urlpatterns = [
  path('', views.index, name='index')
]