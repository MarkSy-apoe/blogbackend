# Generated by Django 4.2.4 on 2024-01-01 12:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blogpost', '0004_section_remove_post_body_remove_post_slug_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='date_comented'),
            preserve_default=False,
        ),
    ]
