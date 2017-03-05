import json

from django.db import models

class StateManager(models.Manager):
    def status_json(self, repos, g):
        return json.dumps([s.status_entry(repos, g) for s in self.all()])
