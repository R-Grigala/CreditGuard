from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    censored_number = models.CharField(max_length=16)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.title
