# Generated by Django 4.2.4 on 2024-01-01 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogpost', '0008_remove_comment_email_alter_comment_name_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='breif',
            field=models.TextField(default='test write up'),
            preserve_default=False,
        ),
    ]
