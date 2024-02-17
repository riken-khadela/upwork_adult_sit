from django.core.management.base import BaseCommand, CommandError
from main.models import configuration as conf
from scrapping.settings import BASE_DIR
from mail import SendAnEmail
from bot import scrapping_bot

class Command(BaseCommand):
    help = "Closes the specified poll for voting"


    def handle(self, *args, **options): 
        
        # try:
            bot = scrapping_bot(brazzers_bot=True)
            if bot.starting_bots():
                bot.naughty_ame()
            else:
                SendAnEmail('Could not open up the driver')
                return
            
            
            ...
        # except Exception as e :
        #         SendAnEmail(f'Got an error while processing the downloading process the videos of naughty america!\nError : {e}')