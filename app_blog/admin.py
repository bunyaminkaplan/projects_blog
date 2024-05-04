from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.following_tracker)
admin.site.register(models.user_post)
#admin.site.register(models.load_image)
admin.site.register(models.suggests)
admin.site.register(models.load_image)
admin.site.register(models.image_and_specs)