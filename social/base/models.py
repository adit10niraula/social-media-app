from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follow = models.ManyToManyField("self", related_name="followed_by", symmetrical=False,blank=True)
    date_modified = models.DateTimeField(User, auto_now = True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images")
    profile_bio = models.CharField(null=True, blank=True, max_length=500)
    homepage_link = models.CharField(null=True, blank=True, max_length=500)
    instagram_link = models.CharField(null=True, blank=True, max_length=500)
    linkedin_link = models.CharField(null=True, blank=True, max_length=500)
    
    def get_image_url(self):
        if self.image:
            return self.image.url
        else:
            return f'{settings.MEDIA_URL}defaults/profile.jpg'
    
    def __str__(self):
        return self.user.username
    
#create profile when new user sing up instance

def create_profile (sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user= instance)
        user_profile.save()
        # have user follow himself
        user_profile.follow.set([instance.profile.id])
        user_profile.save()
        

post_save.connect(create_profile, sender=User)

class Twitter(models.Model):
    user = models.ForeignKey(User, related_name="tweet", on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="tweet_like", blank=True)
    
    
    #keep count of likes
    def number_of_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return (f"{self.user}  " f"{self.body[0:50]}...")
    