from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os, pandas as pd
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime
from numpy import delete
import pytz 
from .models import videos_collection

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    folder_path = 'downloads'
    video_extensions = ["mp4", "avi", "mkv", "mov", "wmv","webm"]
    video_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_ext = file.split('.')[-1]
            for ext in video_extensions: 
                if file_ext == ext: 
                    video_files.append(os.path.join(root, file))

    df = pd.read_csv('brazzers_videos_details.csv')
    for video_file in video_files:
        video_name = str(video_file).split('/')[-1]
        print(video_name)
        if len(df[df['Video-name'] == video_name]) == 0:
            os.remove(video_file)
        else:
            if not videos_collection.objects.filter(Video_name=video_name):
                video_data = df[df['Video-name'] == video_name].to_dict(orient='records')[0]
                video_data_dict = {
                    'Video_name': video_data.get('Video-name', None),
                    'Release_Date': timezone.make_aware(datetime.strptime(video_data['Release-Date'], "%B %d, %Y"),pytz.timezone('Asia/Kolkata')),
                    'Poster_Image_uri': video_data.get('Poster-Image_uri', None),
                    'Likes': video_data.get('Likes', None),
                    'Disclike': video_data.get('Disclike', None),
                    'Url': video_data.get('Url', None),
                    'Title': video_data.get('Title', None),
                    'Discription': video_data.get('Discription', None),
                    'Pornstarts': video_data.get('Pornstarts', None),
                }
                print(video_data_dict)
                # breakpoint()
                video_obj = videos_collection.objects.create(**video_data_dict)
                print(video_obj.Video_name)

    for video_obj in videos_collection.objects.all():
        if df[df['Video-name'] == video_obj.Video_name].empty:
            video_obj.delete()

@receiver(post_delete,sender=videos_collection)
def videos_collection_post_delete(sender, instance, **kwargs):
    df = pd.read_csv('brazzers_videos_details.csv')
    video = os.listdir('downloads')
    video_name = instance.Video_name
    name = [i for i in video if i == video_name][0]
    if name:os.remove(f'{os.getcwd()}/downloads/{name}')
    df.drop(df[df['Video-name'] == video_name].index, inplace=True)
    df.to_csv('brazzers_videos_details.csv',index=False)

            
