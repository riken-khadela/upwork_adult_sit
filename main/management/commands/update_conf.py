from django.core.management.base import BaseCommand, CommandError
from main.models import configuration as conf
from scrapping.settings import BASE_DIR
from mail import SendAnEmail

class Command(BaseCommand):
    help = "Closes the specified poll for voting"


    def handle(self, *args, **options): 
        from bot import scrapping_bot
        from utils import close_every_chrome
        logggg = False
        for _ in range(1):
            try:
                # close_every_chrome()
                bot = scrapping_bot(brazzers_bot=True)
                driver = bot.starting_bots()
                if not driver :
                    SendAnEmail('Could not open up the driver')
                    return
                # if bot.naughty_ame():
                    ...
                    
                if bot.brazzers_login() :
                    logggg = True
                    bot.brazzers_get_categories()
                    video_dict = bot.brazzers_get_videos_url()
                    bot.brazzers_download_video(video_dict)
                    tags_102 = bot.get_videos_url(url='https://site-ma.brazzers.com/scenes?addon=102')
                    bot.download_videos(tags_102)
                    tags_152 = bot.get_videos_url(url='https://site-ma.brazzers.com/scenes?addon=152')
                    bot.download_videos(tags_152)
                    tags_162 = bot.get_videos_url(url='https://site-ma.brazzers.com/scenes?addon=162')
                    bot.download_videos(tags_162)
                else:
                    SendAnEmail('Could not logged in into Brazzers')
                print('Vip 4k process')
                if bot.vip4k_login():
                    logggg = True
                    videos_collection_dict = bot.vip4k_get_video(url='https://members.vip4k.com/en/channels/black4k')
                    bot.vip4k_download_video(videos_collection_dict)
                else :
                    SendAnEmail('Could not logged in into Vip 4k')

                if bot.login_Handjob_TV():
                    logggg = True
                    bot.handjob_get_video()
                else:
                    SendAnEmail('Could not logged in into Handjob TV')
                    
                bot.CloseDriver()
                if logggg == True:break
                
            except Exception as e :
                print(e)
                SendAnEmail(f'Got an error while processing the downloading process the videos!\nError : {e}')