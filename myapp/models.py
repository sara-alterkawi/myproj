# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
import uuid

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

class User(AbstractUser):
    id = models.CharField(
         primary_key=True,
         default=uuid.uuid4,
         editable=False,
         max_length=180)
    for letter in letters:
        locals()[letter] = models.IntegerField(default=10)

class OrderHistory(models.Model):
    class Status(models.TextChoices):
        ORDER_CONFIRMED = 'ORDER_CONFIRMED', 'ORDER_CONFIRMED'
        COMPLETED = 'Completed', 'Completed'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,  
        choices=Status.choices,
        default=None,  
        null=True,
        blank=True,)
    
    is_error = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.now)
    user_name = models.CharField(max_length=160)
    error = models.CharField(max_length=120, null=True, default=None)
    status = models.CharField(max_length=100, default='pending')
    click_data = models.JSONField(null=True, blank=True)  # New field for storing click_data
    for letter in letters:
        locals()[letter] = models.IntegerField(null=True, blank=True)
