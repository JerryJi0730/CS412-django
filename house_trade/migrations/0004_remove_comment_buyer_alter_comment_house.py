# Generated by Django 5.1.3 on 2024-12-10 02:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house_trade', '0003_buyer_description_buyer_photo_comment_buyer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='buyer',
        ),
        migrations.AlterField(
            model_name='comment',
            name='house',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='house_trade.house'),
        ),
    ]
