from django.db import models
from authentication.models import User

class Community(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community_name = models.CharField(max_length=300)
    header_image = models.ImageField(upload_to="community_header_images/")
    description = models.TextField()
    members = models.ManyToManyField(User, blank=True, related_name="members_of_community")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.community_name
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=400)
    image_file = models.ImageField(upload_to="uploaded_user_images/")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

class PostComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    actual_comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.actual_comment
