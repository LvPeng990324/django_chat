# Generated by Django 3.2.7 on 2021-10-15 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('File', '0002_auto_20211009_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatfile',
            name='file',
            field=models.FileField(help_text='聊天文件', upload_to='chat_file', verbose_name='聊天文件'),
        ),
    ]
