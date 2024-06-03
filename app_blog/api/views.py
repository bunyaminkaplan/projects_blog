from rest_framework import generics , status
from app_blog.api import serializers as api_serializers
from app_blog import models
from django.contrib.auth.models import User
from rest_framework.response import Response

class user_posts_concrete_view(generics.ListCreateAPIView):
    queryset = models.user_post.objects.all()
    serializer_class = api_serializers.user_post_serializer

class user_posts_detail_view(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.user_post.objects.all()
    serializer_class = api_serializers.user_post_serializer

class aio_concrete_view(generics.ListCreateAPIView):
    queryset = models.image_and_specs.objects.all()
    serializer_class = api_serializers.aio_model_serializer

class aio_summarized_concrete_view(generics.ListCreateAPIView):
    queryset = models.image_and_specs.objects.all()
    serializer_class = api_serializers.aio_model_serializer_summarized

class aio_retupdes_view(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.image_and_specs.objects.all()
    serializer_class = api_serializers.aio_model_serializer_summarized

class image_concrete_view(generics.ListCreateAPIView):
    queryset = models.load_image.objects.all()
    serializer_class = api_serializers.user_image_serializer

class image_retupdes_view(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.load_image.objects.all()
    serializer_class = api_serializers.user_image_serializer

class suggests_concrete_view(generics.ListAPIView):
    queryset = models.suggests.objects.all()
    serializer_class = api_serializers.suggests_serializer

class following_tracker_concrete_view(generics.ListCreateAPIView):
    queryset = models.following_tracker.objects.all()
    serializer_class = api_serializers.following_tracker_serializer

class following_tracker_detail_concrete_view(generics.RetrieveUpdateDestroyAPIView):

    queryset = models.following_tracker.objects.all()
    serializer_class = api_serializers.following_tracker_serializer

    def perform_update(self, serializer):
        tracker_id = self.kwargs.get('pk')
        try:
            modify_tracker = models.following_tracker.objects.get(pk = tracker_id)   
            if modify_tracker.still == True:
                modify_tracker.still = False
            else: 
                modify_tracker.still = True
                modify_tracker.save()   
        except:
            
            return Response(status= status.HTTP_400_BAD_REQUEST)

        print(self.get_object().request_owner)
        serializer.save()
 