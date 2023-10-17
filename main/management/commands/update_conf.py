from django.core.management.base import BaseCommand, CommandError
from main.models import configuration as conf


class Command(BaseCommand):
    help = "Closes the specified poll for voting"


    def handle(self, *args, **options): 
        print('12233232')
        