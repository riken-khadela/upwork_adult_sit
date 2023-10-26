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
                # bot.connect_cyberghost_vpn()
                if bot.brazzers_login() :
                    logggg = True
                    bot.brazzers_get_categories()
                    bot.brazzers_get_videos_url()
                    bot.brazzers_download_video()
                    tags_152 = bot.get_videos_url(url='https://site-ma.brazzers.com/scenes?addon=152')
                    bot.download_videos(tags_152)
                    tags_162 = bot.get_videos_url(url='https://site-ma.brazzers.com/scenes?addon=162')
                    bot.download_videos(tags_162)
                    break

                bot.CloseDriver()
                if logggg == True:break