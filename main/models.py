from curses.ascii import isdigit
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
    def __str__(self) -> str:
        video_title = ""
        video_name_li = self.Video_name.split('_')
        if video_name_li[0] == 'scene' and isdigit(video_name_li[1]) :
            video_title += 'brazzers'

        video_title += self.Video_name
        return video_title