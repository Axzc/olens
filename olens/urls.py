from django.contrib import admin
from django.urls import path, include, re_path
import user.urls
import article.urls

urlpatterns = [
    path('', include(article.urls)),
    path('user/', include(user.urls)),
    path('admin/', admin.site.urls),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),

]