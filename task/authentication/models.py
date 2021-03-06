from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    """
    User Manager for custom user model
    """
    def create_user(self, email, password):
        if password is None:
            raise TypeError("Password should not be none")
        if email is None:
            raise TypeError("User should have a Email")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    """
    Custom user model for auth
    """
    username = None
    email = models.EmailField(max_length=255, unique=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    # get token
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token),
        }
