# Dashboard Stats site


## Getting Started

- Install git on your system.
- Run `git clone gitlab@gitlab.redwerk.com:redwerk/stats_dashboard.git`.
- Enter into the project directory `stats_dashboard/config`.
- Create `config.py` file based on `config.sample.py`
- Build static files - go to `dashboard/static` and run command `grunt build`
- Run development server `source env/bin/activate; flask run`
  and open this link `http://127.0.0.1:5000` in yor web browser.


## Code style and contribution guide
- Install the editorconfig plugin for your code editor.
- Do not copypaste, do not hack, always look for easiest solutions.
- Write tests for your code.
- For every task create a branch from current master, when ready create a merge request back to master.
- Prefer small commits and branches.


## Requirements
Python - 3.4.3
Cython - 0.25.1
flake8 - 3.2.1
Flask - 0.11.1
Flask-Admin - 1.4.2
Flask-Login - 0.4.0
Flask-SQLAlchemy - 2.1
gunicorn - 19.6.0
itsdangerous - 0.24
Jinja2 - 2.8
MarkupSafe - 0.23
mccabe - 0.5.3
mimerender - 0.6.0
oursql3 - 0.9.4
pycodestyle - 2.2.0
pycountry - 17.1.8
pyflakes - 1.3.0
python-dateutil - 2.6.0
python-mimeparse - 1.6.0
six - 1.10.0
SQLAlchemy - 1.1.4
Werkzeug - 0.11.11
WTForms - 2.1

## The structure of the project
    └─ dashboard
        ├─ models      - folder with sqlalchemy models for project application
        ├─ static      - folder with static files only for project application        
        ├─ templates   - folder with the global templates (layouts). Application templates to be stored in the app folder