# Generated by Django 2.2.5 on 2019-12-02 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quora', '0013_auto_20191202_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(default=None, upload_to='Quora/static/images/'),
        ),
    ]
