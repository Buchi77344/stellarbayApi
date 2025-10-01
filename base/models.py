from django.db import models



# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User Model
class CustomUser(AbstractUser):
    # Additional fields for our platform

    pass



from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class APIEndpoint(models.Model):
    METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('PATCH', 'PATCH'),
        ('DELETE', 'DELETE')
    ]
    
    name = models.CharField(max_length=200)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    url = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.method} {self.name}"

class APIRequestLog(models.Model):
    endpoint = models.ForeignKey(APIEndpoint, on_delete=models.CASCADE, related_name='logs', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.CharField(max_length=10)
    url = models.CharField(max_length=500)
    status_code = models.IntegerField(null=True, blank=True)
    response_time = models.FloatField(help_text="Response time in milliseconds")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.method} {self.url} - {self.status_code}"

class DashboardStats(models.Model):
    total_endpoints = models.IntegerField(default=0)
    total_requests = models.IntegerField(default=0)
    success_rate = models.FloatField(default=0.0)
    avg_response_time = models.FloatField(default=0.0)
    calculated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Dashboard Stats"
    
    def __str__(self):
        return f"Stats from {self.calculated_at}"