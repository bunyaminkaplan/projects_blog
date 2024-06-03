from django.urls import path
from app_blog.api import views as api_views

urlpatterns = [
    path( 'user_posts', api_views.user_posts_concrete_view.as_view()),
    path( 'aio' , api_views.aio_concrete_view.as_view() , name= 'aio'),
    path( 'aio_2' , api_views.aio_summarized_concrete_view.as_view() , name='aio_2'),
    path( 'aio_2/<int:pk>' , api_views.aio_retupdes_view.as_view() , name= "aio_retupdes"),
    path( 'user_posts/<int:pk>' , api_views.user_posts_detail_view.as_view() , name= 'user_posts_detail'),
    path( 'images' , api_views.image_concrete_view.as_view() , name= 'images'), 
    path( 'images/<int:pk>' , api_views.image_retupdes_view.as_view() , name= 'images_retupdes'), 
    path( 'suggests' , api_views.suggests_concrete_view.as_view() , name= 'suggests'),
    path( 'following_trackers' , api_views.following_tracker_concrete_view.as_view() , name= 'following_tracker'),
    path( 'following_trackers/<int:pk>' , api_views.following_tracker_detail_concrete_view.as_view() , name='following_tracker_detail'),
]