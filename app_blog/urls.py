from . import views , models
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static


app_name = 'app_blog'

urlpatterns = [
    path('home/' , views.home , name='home'),
    path('add/' , views.add , name='add'),
    path('signup/' , views.user_signup.as_view() , name='user_signup'),
    path('accounts/profile/' , views.redirect_to_home , name='redirect_to_home'),
    path('follow_unfollow/<str:username>' , views.follow_unfollow , name='follow_unfollow'),
    path('delete/<int:gen_code>' , views.delete_post , name='delete_post'),
    path('api_server/' , include('app_blog.api.urls')),
 
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)