from django.core.management.base import BaseCommand
from github import Github
from dashboard.apps.hub.models import State
import os
import sys

class Command(BaseCommand):
    help = ("Creates a json file of the project status of each state to be "
            "consumedbye the front-end website.")

    def handle(self, *args, **options):
        # TODO: Allow for token to be in settings as well as Environment Variable?
        token = os.environ.get('GITHUB_TOKEN')
        if token is None:
            sys.stderr.write('GITHUB_TOKEN not defined; rate-limiting will apply.')

        # Create connection to Github and get list of repos
        g = Github(os.environ.get('GITHUB_TOKEN'))
        repos = g.get_organization("openelections").get_repos()
        self.stdout.write(State.objects.status_json([r.name for r in repos], g))
