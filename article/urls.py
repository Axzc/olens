from django.urls import path
from article import views
from article.views import IndexView

urlpatterns = [
  path('', IndexView.as_view(), name='index'),
  path('home', views.home, name='home')
]