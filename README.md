# Dashboard Stats site


## Getting Started

- Install git, virtualbox and vagrant on your system.
- Run `git clone gitlab@gitlab.redwerk.com:JA/justin-alexander-python.git`.
- Enter into the project directory `justin-alexander-python`.
- Run `vagrant up`.
- Run `vagrant ssh`.
- Run `ja-python/bin/install.sh`, use this command only for project deploy.
- Run django development server `source env/bin/activate; python ja-python/manage.py runserver 0.0.0.0:8888`
  and open this link `http://0.0.0.0:8888` in yor web browser.
- Run `vagrant halt` to stops the vagrant machine and `vagrant reload` to reload.


## Code style and contribution guide
- Install the [editorconfig](http://editorconfig.org/) plugin for your code editor.
- Do not copypaste, do not hack, always look for easiest solutions.
- Write tests for your code.
- For every task create a branch from current `master`, when ready create a merge request back to `dev`.
- Prefer small commits and branches.
- Don't update files in `static/modules/external` from `justin-alexander-frontend` repositories.
- Read this [docs](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/).


## Requirements

- Python >= 3.4.1
- Django 1.10.1
- PostgreSQL 9.5.3
- Redis
- Virtualenv 15.0.1
- Virtualbox
- Vagrant


### Decision psycopg2 installation problems in Linux/Ubuntu system
http://stackoverflow.com/questions/22938679/error-trying-to-install-postgres-for-python-psycopg2


### Table thumbnail_kvstore doesn't exist
http://stackoverflow.com/questions/35136411/table-thumbnail-kvstore-doesnt-exist


## The structure of the project

    └─ dashboard
        ├─ config    - module settings. For each environment uses a different configuration file.
        ├─ static      - folder with static files only for project applications
        ├─ mixin       - mixins classes
        ├─ generic     - base validators, widgets and fields
        ├─ static_collected - STATIC_ROOT folder where all the files are copied with collectstatic.These files
        |                     do not need to be added to the project repository
        ├─ templates   - folder with the global templates (layouts). Application templates to be stored in the app folder