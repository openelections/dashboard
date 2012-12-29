import os
import sys
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dashboard.config.prod.settings")
sys.path.append(settings.PROJECT_ROOT)
sys.path.append(os.path.join(settings.PROJECT_ROOT,'apps'))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
