# Generated by Django 2.2.5 on 2019-12-02 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quora', '0012_post_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='Quora/static/images/'),
        ),
    ]
