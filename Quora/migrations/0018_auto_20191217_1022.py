# Generated by Django 2.2.5 on 2019-12-17 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quora', '0017_user_topics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='topics',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]