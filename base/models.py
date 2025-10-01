from django.db import models



# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User Model
class CustomUser(AbstractUser):
    # Additional fields for our platform

    pass