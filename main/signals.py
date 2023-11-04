from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os, pandas as pd
from dateutil import parser
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime
from numpy import delete
import pytz 
from .models import videos_collection, configuration

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    folder_path = 'downloads'
    video_extensions = ["mp4", "avi", "mkv", "mov", "wmv","webm"]
    video_files = []
    for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                print(filename)
                base_name, extension = os.path.splitext(filename)
                if extension == '.mp4':
                    video_files.append(os.path.join(foldername, filename))
    dfs = []

    for obj in configuration.objects.all():
        df = pd.read_csv(os.path.join(os.getcwd(),f'{obj.website_name}_videos_details.csv'))
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    df[['Likes']] = df[['Likes']].fillna(0)
    df[['Disclike']] = df[['Disclike']].fillna(0)
    for video_file in video_files:
        video_name = str(video_file).split('/')[-1]
        
        if len(df[df['Video-name'] == video_name]) == 0:
            if video_file.endswith('.mp4') or video_file.endswith('.jpg'):
                os.remove(video_file)
        else:
            if not videos_collection.objects.filter(Video_name=video_name):
                video_data = df[df['Video-name'] == video_name].to_dict(orient='records')
                if video_data:
                    video_data_dict = {
                        'Video_name': video_data[0].get('Video-name', None),
                        'Release_Date': timezone.make_aware(parser.parse(video_data[0]['Release-Date']),pytz.timezone('Asia/Kolkata')),
                        'Poster_Image_uri': video_data[0].get('poster_download_uri', None),
                        'Likes': video_data[0].get('Likes', 0),
                        'Disclike': video_data[0].get('Disclike', 0),
                        'Url': video_data[0].get('video_download_url', None),
                        'Title': video_data[0].get('Title', None),
                        'Discription': video_data[0].get('Discription', None),
                        'Pornstarts': video_data[0].get('Pornstarts', None),
                    }
                    videos_collection.objects.update_or_create(**video_data_dict)
            
        for video_obj in videos_collection.objects.all():
            if video_obj.Video_name not in df['Video-name'].values:
                video_obj.delete()

@receiver(post_delete,sender=videos_collection)
def videos_collection_post_delete(sender, instance, **kwargs):
    video_name = instance.Video_name
    base_name = str(video_name).split('.')[0]
    for foldername, subfolders, filenames in os.walk(os.path.join(os.getcwd(),'downloads')):
        for filename in filenames:
            if os.path.splitext(os.path.basename(filename))[0] == base_name:
                os.remove(os.path.join(foldername, filename))

    for obj in configuration.objects.all():
        df = pd.read_csv(os.path.join(os.getcwd(),f'{obj.website_name}_videos_details.csv'))
        if video_name in  df['Video-name'].values:
            df.drop(df[df['Video-name'] == video_name].index, inplace=True)
            df.to_csv(os.path.join(os.getcwd(),f'{obj.website_name}_videos_details.csv'),index=False)

            
