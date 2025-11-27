from django.contrib.auth.models import User
from django.db import models


class AuthToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField(null=True, blank=True)
    token_type = models.CharField(max_length=30, null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Token: User '{self.user.username}' - expires_at: {self.expires_at} - access_token: {self.access_token}"
