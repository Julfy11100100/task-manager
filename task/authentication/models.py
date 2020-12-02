from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password):
        if password is None:
            raise TypeError("Password should not be none")
        if email is None:
            raise TypeError("User should have a Email")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = ['email']
    REQUIRED_FIELDS = ['email', 'password']

    objects = UserManager()

    def __str__(self):
        return self.email
