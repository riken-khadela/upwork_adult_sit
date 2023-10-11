from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
import os, pandas as pd
from numpy import delete
from .models import videos_collection

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    folder_path = 'videos'
    video_extensions = ["mp4", "avi", "mkv", "mov", "wmv","webm"]
    video_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_ext = file.split('.')[-1]
            for ext in video_extensions: 
                if file_ext == ext: 
                    video_files.append(os.path.join(root, file))

    df = pd.read_csv('videos_details.csv')
    for video_file in video_files:
        video_name = str(video_file).split('/')[-1]
        if len(df[df['Video-name'] == video_name]) == 0 : 
            os.remove(video_file)
        else :
            if not videos_collection.objects.filter(Video_name=video_name) :
                video_data = df[df['Video-name'] == video_name].to_dict(orient='records')[0]
                videos_collection.objects.create(
                    Video_name = video_data['Video-name'],
                    Release_Date = video_data['Release-Date'],
                    Poster_Image_uri = video_data['Poster-Image_uri'],
                    Likes = video_data['Likes'],
                    Disclike = video_data['Disclike'],
                    Url = video_data['Url'],
                    Title = video_data['Title'],
                    Discription = video_data['Discription'],
                    Pornstarts = video_data['Pornstarts']
                )

    for video_obj in videos_collection.objects.all() :
        video_obj.Video_name
        if not df[df['Video-name'] == video_obj.Video_name] : 
            video_obj.delete()
            
