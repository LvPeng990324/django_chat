# Generated by Django 3.2.7 on 2021-10-07 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0003_session_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatlog',
            name='content',
            field=models.JSONField(help_text='内容', verbose_name='内容'),
        ),
    ]
