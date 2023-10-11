from django.db import models

# Create your models here.


class videos_collection(models.Model):
    Video_name = models.CharField(max_length=255,null=True, blank=True)
    Release_Date = models.DateTimeField(null=True,blank=True)
    Poster_Image_uri = models.URLField(null=True,blank=True)
    Likes = models.IntegerField(null=True,blank=True)
    Disclike = models.IntegerField(null=True,blank=True)
    Url = models.URLField(null=True,blank=True)
    Title = models.CharField(max_length=255)
    Discription = models.TextField(null=True,blank=True)
    Pornstarts = models.CharField(max_length=500,null=True,blank=True)