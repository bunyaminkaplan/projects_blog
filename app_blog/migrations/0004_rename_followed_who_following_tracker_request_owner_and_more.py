# Generated by Django 5.0.3 on 2024-05-31 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0003_alter_load_image_uploaded_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='following_tracker',
            old_name='request_receiver',
            new_name='request_owner',
        ),
        migrations.RenameField(
            model_name='following_tracker',
            old_name='request_owner',
            new_name='request_receiver',
        ),
    ]