from django.core.management.base import BaseCommand

from dashboard.apps.hub.models import State

class Command(BaseCommand):
    help = ("Creates a json file of the project status of each state to be "
            "consumed be the front-end website.")

    def handle(self, *args, **options):
        self.stdout.write(State.objects.status_json())
