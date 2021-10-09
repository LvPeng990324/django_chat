# Generated by Django 3.2.7 on 2021-10-09 16:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('File', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatfile',
            options={'verbose_name': '聊天文件', 'verbose_name_plural': '聊天文件'},
        ),
        migrations.AddField(
            model_name='chatfile',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='创建时间', verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chatfile',
            name='file',
            field=models.FileField(default='', help_text='聊天文件', upload_to='media/chat_file', verbose_name='聊天文件'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chatfile',
            name='md5',
            field=models.CharField(default='', help_text='文件md5', max_length=32, verbose_name='文件md5'),
            preserve_default=False,
        ),
    ]