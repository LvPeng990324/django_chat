# Generated by Django 3.2.7 on 2021-10-09 15:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0004_alter_chatlog_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='recently_active_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='最近活跃时间', verbose_name='最近活跃时间'),
            preserve_default=False,
        ),
    ]