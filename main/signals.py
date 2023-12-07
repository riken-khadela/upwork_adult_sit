from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os, pandas as pd
from django.conf import settings
from dateutil import parser
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime
from numpy import delete
from collections import defaultdict
import pytz 
from .models import videos_collection, configuration

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    base_name_dict = defaultdict(list)
    for foldername, subfolders, filenames in os.walk(os.path.join(os.getcwd(), 'downloads')):
        for filename in filenames:
            base_name = os.path.splitext(os.path.basename(filename))[0]
            if os.path.basename(filename).endswith('.mp4') or os.path.basename(filename).endswith('.jpg'):
                base_name_dict[base_name].append(os.path.join(foldername, filename))
    for base_name, file_list in base_name_dict.items():
        if len(file_list) == 1:
            os.remove(file_list[0])
    folder_path = 'downloads'
    video_extensions = ["mp4", "avi", "mkv", "mov", "wmv","webm"]
    video_files = []
    for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                base_name, extension = os.path.splitext(filename)
                if extension == '.mp4':
                    video_files.append(os.path.join(foldername, filename))
    dfs = []    
    csv_root = settings.CSV_ROOT
    files = os.listdir(csv_root)
    for file in files:
        if file.endswith('_details.csv'):
            df = pd.read_csv(os.path.join(csv_root,file))
            dfs.append(df)
    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        df[['Likes']] = df[['Likes']].fillna(0)
        df[['Disclike']] = df[['Disclike']].fillna(0)
        for video_file in video_files:
            video_name = str(video_file).split('/')[-1]
            
            if len(df[df['Video-name'] == video_name]) == 0:
                if video_file.endswith('.mp4') or video_file.endswith('.jpg'):
                    os.remove(video_file)
            else:
                # if not videos_collection.objects.filter(Video_name=video_name):
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
                            'Category': video_data[0].get('Category', None),
                        }
                        videos_collection.objects.update_or_create(**video_data_dict)

        csv_root = settings.CSV_ROOT
        files = os.listdir(csv_root)
        video_fil = [str(video).split('/')[-1] for video in video_files ]
        for file in files:
            if file.endswith('_details.csv'):
                df = pd.read_csv(os.path.join(csv_root,file))
                df = df[df['Video-name'].isin(video_fil)]
                df.to_csv(os.path.join(csv_root,file),index=False)

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
                try:
                    os.remove(os.path.join(foldername, filename))
                except:pass

    csv_root = settings.CSV_ROOT
    files = os.listdir(csv_root)
    for file in files:
        if file.endswith('_details.csv'):
            df = pd.read_csv(os.path.join(csv_root,file))
            if video_name in  df['Video-name'].values:
                df.drop(df[df['Video-name'] == video_name].index, inplace=True)
                df.to_csv(os.path.join(csv_root,file),index=False)

            
