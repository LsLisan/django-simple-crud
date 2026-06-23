from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150)
    age = models.PositiveIntegerField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    