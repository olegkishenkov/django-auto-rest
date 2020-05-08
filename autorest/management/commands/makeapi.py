import os

import django.apps
import django.conf
from django.core.management import BaseCommand
from django.template import Engine, Context


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
            absolute_dir = os.path.join(django.conf.settings.BASE_DIR, 'autorest')
            old_path = os.path.join(absolute_dir, 'management', 'commands', 'automatic_urls.py-tpl')
            with open(old_path, encoding='utf-8') as template_file:
                content = template_file.read()
            template = Engine().from_string(content)
            models_ = []
            for model in models:
                if model.__name__.lower().endswith('y'):
                    lower_case_name_plural = model.__name__.lower().rstrip('y') + 'ies'
                else:
                    lower_case_name_plural = model.__name__.lower() + 's'
                models_.append(
                    {
                        'name': model.__name__,
                        'lower_case_name_plural': lower_case_name_plural,git
                        'module': model.__module__,
                        'fields': [field.name for field in model._meta.fields],
                    }
                )
            context = Context({
                **options,
                'models': models_,
            }, autoescape=False)

            content = template.render(context)
            new_path = os.path.join(absolute_dir, 'automatic_urls.py')
            with open(new_path, 'w', encoding='utf-8') as new_file:
                new_file.write(content)
        models_string = ' '.join([str(model.__name__) for model in models])
        self.stdout.write(self.style.SUCCESS('a REST API created for models {}'.format(models_string)))
