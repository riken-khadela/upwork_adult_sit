from django.core.management.base import BaseCommand, CommandError
import pandas as pd, os

class Command(BaseCommand):
    help = "Closes the specified poll for voting"


    def handle(self, *args, **options): 
        df = pd.read_csv(os.path.join(os.getcwd(),'brazzers_videos_details.csv'))
        for i in df.index:
            df.at[i, 'video_download_url'] = df.at[i, 'video_download_url'].rstrip('/')
            df.at[i, 'poster_download_uri'] = df.at[i, 'poster_download_uri'].rstrip('/')

        # Save the modified DataFrame back to the CSV file
        df.to_csv(os.path.join(os.getcwd(), 'brazzers_videos_details.csv'), index=False)
        df = pd.read_csv(os.path.join(os.getcwd(),'brazzers_videos.csv'))
        for i in df.index:
            df.at[i, 'video_url'] = df.at[i, 'video_url'].rstrip('/')
        df.to_csv(os.path.join(os.getcwd(), 'brazzers_videos.csv'), index=False)

