# Generated by Django 5.0.3 on 2024-05-29 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0002_alter_load_image_local_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='load_image',
            name='uploaded_url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
