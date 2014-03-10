import json

from django.db import models

class StateManager(models.Manager):
    def status_json(self):
        return json.dumps([s.status_entry() for s in self.all()])
