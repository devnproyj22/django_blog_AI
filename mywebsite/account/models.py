from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	nickname = models.CharField(max_length=50, unique=True)
	email = models.EmailField(unique=True)
