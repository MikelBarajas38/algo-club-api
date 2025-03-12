"""
Database models.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """
    Manager for custom user model.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create, save and return a new user.
        """
        if not email:
            raise ValueError('Email is required.')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Create, save and return a new superuser.
        """
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    codeforces_handle = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True
    )
    omegaup_handle = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True
    )
    kattis_handle = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'  # Default field for authentication


class Contest(models.Model):
    """
    Contest model.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField()

    PLATFORMS = {
        'C': 'Codeforces',
        'O': 'OmegaUp',
        'K': 'Kattis',
        'V': 'Vjudge'
    }

    platform = models.CharField(
        max_length=1,
        choices=PLATFORMS
    )

    platform_id = models.CharField(max_length=10)

    start_time = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )

    end_time = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )

    last_updated = models.DateTimeField(
        auto_now=True,
        blank=True
    )

    def __str__(self):
        return self.name
