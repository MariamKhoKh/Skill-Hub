from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = models.CharField(max_length=10, choices=ROLES)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.role}"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
