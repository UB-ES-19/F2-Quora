# Generated by Django 2.2.5 on 2019-10-15 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Quora', '0002_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
    ]
