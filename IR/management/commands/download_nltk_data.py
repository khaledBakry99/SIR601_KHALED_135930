from django.core.management.base import BaseCommand
import nltk

class Command(BaseCommand):
    help = 'Download NLTK data'

    def handle(self, *args, **options):
        nltk.download('punkt')
        self.stdout.write(self.style.SUCCESS('Successfully downloaded NLTK data'))
        # python manage.py download_nltk_data
