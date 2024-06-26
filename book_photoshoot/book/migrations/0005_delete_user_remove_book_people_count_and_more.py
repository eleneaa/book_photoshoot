# Generated by Django 5.0.3 on 2024-05-05 15:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_user_rename_user_book_user_name_remove_book_time_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.RemoveField(
            model_name='book',
            name='people_count',
        ),
        migrations.RemoveField(
            model_name='book',
            name='photo_studio',
        ),
        migrations.RemoveField(
            model_name='book',
            name='user_name',
        ),
        migrations.AddField(
            model_name='book',
            name='number',
            field=models.CharField(default=0, max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
