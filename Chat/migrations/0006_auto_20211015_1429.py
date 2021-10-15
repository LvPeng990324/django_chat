# Generated by Django 3.2.7 on 2021-10-15 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0005_session_recently_active_time'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='chatlog',
            index=models.Index(fields=['create_time'], name='Chat_chatlo_create__ba4dbb_idx'),
        ),
        migrations.AddIndex(
            model_name='chatuser',
            index=models.Index(fields=['user_id'], name='Chat_chatus_user_id_12e618_idx'),
        ),
    ]
