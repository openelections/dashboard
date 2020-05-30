OpenElections Dashboard
=======================

OpenElections Dashboard is a clearinghouse for state election data.
The Dashboard will feature information about election agencies, sources of certified
results, and the status of the project's data gathering operation.

# NOTE: THIS REPOSITORY WILL BE DEPRECATED AND REPLACED WITH ONE THAT CONTAINS METADATA FILES

Getting started as a developer
------------------------------

### Prerequisites (on Ubuntu 18.04)

```bash
$ sudo apt-get install libpq-dev memcached
```

### Setup

Create a virtualenv

```bash
$ virtualenv openelections
```

Jump in and activate

```bash
$ cd openelections
$ . bin/activate
```

Clone the repository and jump in

```bash
$ git clone git@github.com:openelections/dashboard.git repo
$ cd repo
```

Install the python dependencies

```bash
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
```

Add the ``dashboard`` directory to your PYTHONPATH

```bash
$ export PYTHONPATH=$PYTHONPATH:`pwd`/dashboard
```

Create a ``local_settings.py`` from the template

```bash
$ cp dashboard/config/local_settings.py.tmpl dashboard/config/local_settings.py
```

Edit the local settings with your database name and secret key

```bash
$ vim dashboard/config/local_settings.py
```

Create the database.

```bash
# Here's using the default postgresql backend and database name
$ sudo -u postgres createdb openelections-dashboard
```

Sync the database and catch up with all the migrations

```bash
$ export DJANGO_SETTINGS_MODULE=dashboard.config.dev.settings
$ django-admin.py syncdb
$ django-admin.py migrate hub
```

Load initial metadata

```bash
$ django-admin.py loaddata dashboard/apps/hub/fixtures/initial_metadata.json
```

Fire up the development server

```bash
$ django-admin.py runserver
```
