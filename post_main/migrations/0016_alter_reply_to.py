# Generated by Django 3.2.5 on 2021-08-06 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post_main', '0015_auto_20210806_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tocomment', to='post_main.reply'),
        ),
    ]
