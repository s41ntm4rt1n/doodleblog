from django.db import models
import os, random, secrets
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings


class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)
    
    
    USERNAME_FIELD=('email')
    REQUIRED_FIELDS=['username']
    
    def __str__(self):
        return self.email
    
class OTPToken(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='otps')
    otp_code=models.CharField(max_length=6, default=str(secrets.randbelow(1000000)).zfill(6))
    created_at=models.DateTimeField(auto_now_add=True)
    expires_at=models.DateTimeField( null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    
def user_images_upload_to(instance, filename):
    username = instance.user
    return os.path.join("features", username, filename)