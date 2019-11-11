from django.contrib import admin
from django.urls import path, include
import user.urls
import article.urls

urlpatterns = [
    path('', include(article.urls)),
    path('user/', include(user.urls)),
    path('admin/', admin.site.urls),

]