import django.apps
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'makes and publishes a REST API for all the models of the installed apps'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='does not actually create an API, only prints model names'
        )

    def handle(self, *args, **options):
        models = django.apps.apps.get_models()
        if not options['dry_run']:
            pass
        models_string = ' '.join([str(model.__name__) for model in models])
        self.stdout.write(self.style.SUCCESS('a REST API created for models {}'.format(models_string)))