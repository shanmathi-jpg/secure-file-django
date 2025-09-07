from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds:
      - is_admin: Boolean to track if the user is an admin
      - last_logout: Tracks the user's last logout time
    """
    is_admin = models.BooleanField(default=False)
    last_logout = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username


class File(models.Model):
    """
    Model to store uploaded encrypted files.
    Fields:
      - owner: FK to the user who uploaded
      - filename: Original name of the file
      - encrypted_data: Encrypted content of the file
      - upload_time: Auto-set timestamp of upload
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    filename = models.CharField(max_length=255)
    encrypted_data = models.BinaryField()
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} ({self.owner.username})"
