# Generated by Django 3.2.5 on 2021-08-08 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post_main', '0020_reply_postcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='postcomment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='postcomment_reply', to='post_main.postcomment'),
        ),
    ]
