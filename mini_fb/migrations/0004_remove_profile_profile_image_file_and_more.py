# Generated by Django 5.1.2 on 2024-10-20 19:57

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0003_remove_profile_profile_image_url_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profile_image_file',
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_image_url',
            field=models.URLField(default='http://example.com/default-image.jpg'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(upload_to='images/')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('status_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mini_fb.statusmessage')),
            ],
        ),
    ]
