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
                bot = scrapping_bot(brazzers_bot=False)
                print('adultprime process starting')
                if bot.adultprime_login():
                    logggg = True
                    bot.download_all_adultprime_channels_video()
                else :
                    SendAnEmail('Could not logged in into Vip 4k')

                bot.CloseDriver()
                if logggg == True:break
                
            except Exception as e :
                print(e)
                SendAnEmail(f'Got an error while processing the downloading process the videos!\nError : {e}')