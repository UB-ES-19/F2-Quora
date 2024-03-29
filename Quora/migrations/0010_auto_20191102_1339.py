# Generated by Django 2.2.5 on 2019-11-02 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quora', '0009_remove_user_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='follow',
            name='following',
        ),
        migrations.AddField(
            model_name='follow',
            name='following',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
