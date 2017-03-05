from django.core.management.base import BaseCommand

from github import Github
import sys # remove this

from dashboard.apps.hub.models import State

class Command(BaseCommand):
    help = ("Creates a json file of the project status of each state to be "
            "consumed be the front-end website.")

    def handle(self, *args, **options):
        g = Github("0cba242dc698e71f0947fbf150ed814a0d5ff624")

        repos = g.get_organization("openelections").get_repos()

        self.stdout.write(State.objects.status_json([r.name for r in repos], g))
