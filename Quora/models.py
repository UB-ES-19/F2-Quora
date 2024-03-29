from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.db import models
from datetime import datetime
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
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(('email address'), unique=True)
    photo = models.ImageField(upload_to="Quora/static/images/",
                              default="Quora/static/images/profile_default.png", blank=True, null=True)
    description = models.TextField(default=None, blank=True, null=True)
    topics = models.TextField(default=None, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Follow(models.Model):
    following = models.ManyToManyField(User)
    follower = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="owner")
    follow_time = models.DateTimeField(auto_now=True)


class Post(models.Model):
    """Post model."""
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    question = models.TextField()
    topic = models.TextField(default=None)


class Answer(models.Model):
    """Answer model"""
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=datetime.now)
    original_post = models.ForeignKey(
        Post, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    content = models.TextField()
