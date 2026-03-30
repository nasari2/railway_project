from django.db import models
from django.contrib.auth.models import AbstractUser


# Custom User Model
# workforce/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    role = models.CharField(max_length=10, choices=[('admin','Admin'),('worker','Worker')])
    address = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


# Task Model (Attendance / Work)
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ])
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


# Leave Model
class Leave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )

    def __str__(self):
        return f"{self.user} - {self.status}"
    