# Generated by Django 3.0.4 on 2020-05-26 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Diary', '0002_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(max_length=150),
        ),
    ]
