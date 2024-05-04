from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

app_name = 'app_blog'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_blog.urls')),
    path('' , include('django.contrib.auth.urls'))

]
