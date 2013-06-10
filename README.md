=======================
OpenElections Dashboard
=======================

OpenElections Dashboard is a clearinghouse for state election data.
The Dashboard will feature information about election agencies, sources of certified
results, and the status of the project's data gathering operation.

Getting started as a developer
------------------------------

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

Make a couple of the ``local_settings.py`` template

```bash
$ cp dashboard/config/local_settings.py.tmpl dashboard/config/local_settings.py
```

Edit the local settings with your database name and secret key

```bash
$ vim dashbaord/config/local_settings.py
```

Create the database.

```bash
# Here's using the default postgresql backend and database name
$ sudo -u postgres createdb openelections-dashboard
```

Sync the database and catch up with all the migrations

```bash
$ django-admin.py syncdb
$ django-admin.py migrate hub
```

Fire up the development server

```bash
$ django-admin.py runserver
```
