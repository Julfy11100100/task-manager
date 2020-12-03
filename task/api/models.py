from django.db import models
from authentication.models import User


class Task(models.Model):
    """
    Task model
    """

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120, blank=False)
    text = models.TextField()
    is_complite = models.BooleanField(default=False)
    date = models.DateField(null=False, blank=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


