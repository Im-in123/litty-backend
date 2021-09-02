# Generated by Django 3.2.5 on 2021-08-06 01:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post_main', '0007_auto_20210802_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='comment_like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postcomment',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='post_main.postcomment'),
        ),
    ]