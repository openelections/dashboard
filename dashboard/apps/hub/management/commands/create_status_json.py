from django.core.management.base import BaseCommand

from github import Github
import os

from dashboard.apps.hub.models import State

class Command(BaseCommand):
    help = ("Creates a json file of the project status of each state to be "
            "consumed be the front-end website.")

    def handle(self, *args, **options):
        g = Github(os.environ['GITHUB_TOKEN'])

        repos = g.get_organization("openelections").get_repos()

        self.stdout.write(State.objects.status_json([r.name for r in repos], g))
