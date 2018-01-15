from django.db import models
from django.contrib.auth.models import User
import uuid

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    secretid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Feedback(models.Model):
    url = models.TextField()
    visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
