import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.db import models

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, fullname, email, username, password=None, **kwargs):
        if fullname is None:
            raise TypeError("User must have a fullname.")
        if email is None:
            raise TypeError("User must have an email.")
        if username is None:
            raise TypeError("User must have a username.")
        if password is None:
            raise TypeError("User must have a password.")

        user = self.model(
            fullname=fullname,
            email=self.normalize_email(email),
            username=username,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, fullname, username, email, password, **kwargs):
        if fullname is None:
            raise TypeError("Superuser must have a fullname.")
        if password is None:
            raise TypeError("Superuser must have a password.")
        if email is None:
            raise TypeError("Superuser must have an email.")
        if username is None:
            raise TypeError("Superuser must have an username.")

        user = self.create_user(fullname, email, username, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        is_active = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    fullname = models.CharField(max_length=300)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    keep_logged_in = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["fullname", "email", "is_active", "is_superuser", "is_staff", "keep_logged_in"]

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"
