from app_blog import models
from rest_framework import serializers, generics
from app_blog.api import serializers as api_serializers



class user_post_serializer(serializers.ModelSerializer):   
    class Meta:
        model = models.user_post
        fields = '__all__'       
    
class user_image_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.load_image
        fields = '__all__'

class suggests_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.suggests
        fields = '__all__'

class aio_model_serializer(serializers.ModelSerializer):
    specs = api_serializers.user_post_serializer(read_only = True)
    image = serializers.StringRelatedField(read_only = True)
    class Meta:
        model = models.image_and_specs
        fields = '__all__'

class aio_model_serializer_summarized(serializers.ModelSerializer):
    class Meta:
        model = models.image_and_specs
        fields = '__all__'
    
class following_tracker_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.following_tracker
        fields = '__all__'
