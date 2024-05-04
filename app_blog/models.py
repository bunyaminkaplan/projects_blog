from django.db import models
import os


# Create your models here.

class suggests(models.Model):
    username = models.CharField(max_length=20)



class user_post(models.Model):
    who_pushed = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    index = models.CharField(max_length=100)
    like_count = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)
    image_added = models.BooleanField(default=False)
    generated_code = models.IntegerField()
    


class following_tracker(models.Model):
    who_requested = models.CharField(max_length=20 )
    followed_who = models.CharField(max_length=20 )
    still = models.BooleanField(default=True)





def generate_filename(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f'{instance.current_user_username}_{instance.added_at}.{ext}'
    return os.path.join(f'images/{instance.current_user_username}', new_filename)



class load_image(models.Model):
    added_at = models.DateTimeField(auto_now_add=True)
    import_something = models.ImageField(upload_to=generate_filename)
    current_user_username = models.CharField(max_length=20)
    generated_code = models.IntegerField()
    

class generate_code(models.Model):
    random = models.CharField(max_length=20)



def generate_post_code():
    code_item = generate_code.objects.create(random = 'random')
    return code_item.pk
       


class image_and_specs(models.Model):
    specs = models.ForeignKey(user_post , on_delete=models.CASCADE )
    image = models.ForeignKey(load_image , on_delete=models.CASCADE , blank=True, null=True )
    added_at = models.DateTimeField(auto_now_add=True)
    generated_code = models.IntegerField()
