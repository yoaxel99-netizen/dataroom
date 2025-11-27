import uuid
from django.contrib.auth.models import User
from django.db import models


class Storage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    mimeType = models.CharField(max_length=200)
    file = models.FileField(upload_to='storage')
    uploaded_at = models.DateTimeField(auto_now_add=True)
