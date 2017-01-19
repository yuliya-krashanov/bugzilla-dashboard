import json
import os
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from . import app

bugzilla_engine = create_engine(app.config.get('BUGZILLA_DATABASE_URI', None), convert_unicode=True)
bugzilla_db_sm = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=bugzilla_engine))

settings_engine = create_engine(app.config.get('SETTINGS_DATABASE_URI', None), convert_unicode=True)
settings_db_sm = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=settings_engine))


BugzillaBase = declarative_base(bind=bugzilla_engine)
BugzillaBase.query = bugzilla_db_sm.query_property()

SettingsBase = declarative_base(bind=settings_engine)
SettingsBase.query = settings_db_sm.query_property()

bugzilla_db = bugzilla_db_sm()
settings_db = settings_db_sm()


def with_db(f):
    @wraps(f)
    def new_f(*args, **kwargs):
        try:
            return f(bugzilla_db, settings_db, *args, **kwargs)
        finally:
            bugzilla_db.close()
            settings_db.close()
    return new_f

@with_db
def init_db(bugzilla_db, settings_db, f):
    @wraps(f)
    def decorated_fun(*args, **kwargs):
        import dashboard.models.bugzilla_models as zilla_m, dashboard.models.settings_models as sett_m

        SettingsBase.metadata.create_all(bind=settings_engine)

        projects_zilla = [(p.id, p.name) for p in zilla_m.Product.query.filter(zilla_m.Product.isactive == 1).all()]

        projects_sett = [{'id': p.id, 'project_id': p.bz_project_id} for p in sett_m.Project.query.all()]

        new_projects = [sett_m.Project(bz_project_id=proj_id, name=name) for proj_id, name in projects_zilla
                        if all(pr_s.get('project_id', None) != proj_id for pr_s in projects_sett)]

        if new_projects:
            settings_db.add_all(new_projects)
            settings_db.commit()

        if not settings_db.query(sett_m.Country).count():
            with open(os.path.join(app.config.get('CONFIG_DIR', None), 'countries.json')) as countries_json_data:
                countries_list = json.load(countries_json_data)

            countries = map((lambda country: sett_m.Country(name=country.get('name', None), code=country.get('code', None))),
                            countries_list)
            settings_db.add_all(countries)
            settings_db.commit()

        if not settings_db.query(sett_m.State).count():
            with open(os.path.join(app.config.get('CONFIG_DIR', None), 'states.json')) as states_json_data:
                states_list = json.load(states_json_data)

            us_item = settings_db.query(sett_m.Country).filter_by(name='United States').first()
            states = map((lambda state: sett_m.State(name=state.get('name', None), code=state.get('code', None))),
                         states_list)
            us_item.states.extend(states)
            settings_db.commit()

        return f(*args, **kwargs)

    return decorated_fun
