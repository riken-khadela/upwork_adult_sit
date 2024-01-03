from django.core.management.base import BaseCommand, CommandError
from main.models import configuration as conf
from scrapping.settings import BASE_DIR


class Command(BaseCommand):
    help = "Closes the specified poll for voting"


    def handle(self, *args, **options): 
        from bot import scrapping_bot
        from utils import close_every_chrome
        logggg = False
        for _ in range(500):
            # try:
                # close_every_chrome()
                bot = scrapping_bot(brazzers_bot=True)
                bot.starting_brazzers_bots()
                if False and bot.brazzers_login() :
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
                    
                if bot.vip4k_login():
                    logggg = True
                    # videos_collection_dict = bot.vip4k_get_video(url='https://members.vip4k.com/en/channels/black4k')
                    # bot.vip4k_download_video(videos_collection_dict)

                if bot.login_Handjob_TV():
                    logggg = True
                    bot.handjob_get_video()
                    
                bot.CloseDriver()
                if logggg == True:break