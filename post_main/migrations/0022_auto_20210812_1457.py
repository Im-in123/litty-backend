# Generated by Django 3.2.5 on 2021-08-12 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post_main', '0021_alter_reply_postcomment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='postcomment',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterModelOptions(
            name='reply',
            options={'ordering': ('created_at',)},
        ),
    ]
