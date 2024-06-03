from django.db import models
import os
from django.contrib.auth.models import User

# Create your models here.

class suggests(models.Model):
    username = models.CharField(max_length=20)
    def __str__(self):
        return self.username



class user_post(models.Model):
    who_pushed = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    index = models.CharField(max_length=100)
    like_count = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)
    image_added = models.BooleanField(default=False)
    generated_code = models.IntegerField()
    
    def __str__(self):
        return f"{str(self.generated_code)} --- {self.who_pushed} --- {self.title}"

class following_tracker(models.Model):
    request_owner = models.CharField(max_length=20)
    request_receiver = models.CharField(max_length=20 )
    still = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.request_owner} --> {self.request_receiver} -&- {str(self.still)}"




def generate_filename(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f'{instance.current_user_username}_{instance.added_at.timestamp()}.{ext}'
    return os.path.join(f'images/{instance.current_user_username}', new_filename)



class load_image(models.Model):
    added_at = models.DateTimeField(auto_now_add=True)
    local_url = models.ImageField(upload_to=generate_filename  , blank= True , null= True)
    current_user_username = models.CharField(max_length=20)
    generated_code = models.IntegerField()
    uploaded_url = models.TextField( blank= True , null= True)
    
    def __str__(self):
        return str(self.uploaded_url)

class generate_code(models.Model):
    random = models.CharField(max_length=20)



def generate_post_code():
    code_item = generate_code.objects.create(random = 'random')
    return code_item.pk
       


class image_and_specs(models.Model):
    specs = models.ForeignKey(user_post , on_delete=models.CASCADE , related_name='user_posts_detail')
    image = models.ForeignKey(load_image , on_delete=models.CASCADE , blank=True, null=True , related_name='user_posts_image')
    added_at = models.DateTimeField(auto_now_add=True)
    generated_code = models.IntegerField()

    def __str__(self):
        return str(self.generated_code)

