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
    df[['Likes']] = df[['Likes']].fillna(0)
    df[['Disclike']] = df[['Disclike']].fillna(0)
    for video_file in video_files:
        video_name = str(video_file).split('/')[-1]
        if len(df[df['Video-name'] == video_name]) == 0:
            if video_file.endswith('.mp4') or video_file.endswith('.jpg'):
                os.remove(video_file)
        else:
            # if not videos_collection.objects.filter(Video_name=video_name):
            video_data = df[df['Video-name'] == video_name].to_dict(orient='records')[0]
            video_data_dict = {
                'Video_name': video_data.get('Video-name', None),
                'Release_Date': timezone.make_aware(datetime.strptime(video_data['Release-Date'], "%B %d, %Y"),pytz.timezone('Asia/Kolkata')),
                'Poster_Image_uri': video_data.get('poster_download_uri', None),
                'Likes': video_data.get('Likes', 0),
                'Disclike': video_data.get('Disclike', 0),
                'Url': video_data.get('video_download_url', None),
                'Title': video_data.get('Title', None),
                'Discription': video_data.get('Discription', None),
                'Pornstarts': video_data.get('Pornstarts', None),
            }
            video_obj = videos_collection.objects.update_or_create(**video_data_dict)
    for video_obj in videos_collection.objects.all():
        if video_obj.Video_name not in df['Video-name'].values:
                video_obj.delete()

@receiver(post_delete,sender=videos_collection)
def videos_collection_post_delete(sender, instance, **kwargs):
    df = pd.read_csv('brazzers_videos_details.csv')
    videos = os.listdir('downloads')
    photos = os.listdir('photos')
    video_name = instance.Video_name
    photo_name = str(video_name).replace('.mp4','.jpg')
    video_name = [i for i in videos if i == video_name]
    photo_name = [i for i in photos if i == photo_name]3
    try:
        if video_name:
            os.remove(f'{os.getcwd()}/downloads/{video_name[0]}')
        if photo_name:
            os.remove(f'{os.getcwd()}/photos/{photo_name[0]}')
    except : ...
    if video_name in  df['Video-name'].values:
        df.drop(df[df['Video-name'] == video_name].index, inplace=True)
        df.to_csv('brazzers_videos_details.csv',index=False)

            
