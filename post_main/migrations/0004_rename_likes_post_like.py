# Generated by Django 3.2.5 on 2021-08-01 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post_main', '0003_auto_20210801_1125'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='likes',
            new_name='like',
        ),
    ]
