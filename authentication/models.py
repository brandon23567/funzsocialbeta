from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_bio = models.TextField(max_length=300, null=True, blank=True)
    profile_img = models.ImageField(upload_to="profile_imgs/", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
