from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.db import models
import logging

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(('email address'), unique=True)

    # Should add list of posts

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

from datetime import datetime
class Post(models.Model):
    """Post model."""
    id = models.AutoField(primary_key=True)
    post_date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    #post_answers = [] # array of anwers
    question = models.TextField()
'''
class PostAnswers(models.Model):
    ref_post_id = #?
    answer_content = models.CharField()
    answer_date = models.DateTimeField()
    answer_user = #? user who answers
'''
