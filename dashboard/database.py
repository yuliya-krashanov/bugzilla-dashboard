from functools import wraps
from sqlalchemy import create_engine, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Query, joinedload
import pycountry

from . import app


class BugzillaCustomQuery(Query):
    def actions(self, start_date, end_date, fieldid):
        import dashboard.models.bugzilla_models as bugzilla_models

        return self.join(bugzilla_models.BugsActivity.bug).options(joinedload('bug')).join(bugzilla_models.Bug.product) \
            .filter(
            and_(
                bugzilla_models.BugsActivity.bug_when >= start_date,
                bugzilla_models.BugsActivity.bug_when <= end_date,
                bugzilla_models.BugsActivity.fieldid == fieldid
            ))


bugzilla_engine = create_engine(app.config.get('BUGZILLA_DATABASE_URI', None), convert_unicode=True)
bugzilla_db_sm = scoped_session(sessionmaker(autocommit=False, autoflush=False,
                                             bind=bugzilla_engine, query_cls=BugzillaCustomQuery))

settings_engine = create_engine(app.config.get('SETTINGS_DATABASE_URI', None), convert_unicode=True)
settings_db_sm = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=settings_engine))

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
        import dashboard.models.bugzilla_models as bugzilla_models
        import dashboard.models.settings_models as settings_models

        SettingsBase.metadata.create_all(bind=settings_engine)

        projects_zilla = [(p.id, p.name) for p in
                          bugzilla_models.Product.query.filter(bugzilla_models.Product.isactive == 1).all()]

        projects_sett = [{'id': p.id, 'project_id': p.bz_project_id} for p in settings_models.Project.query.all()]

        new_projects = [settings_models.Project(bz_project_id=proj_id, name=name) for proj_id, name in projects_zilla
                        if all(pr_s.get('project_id', None) != proj_id for pr_s in projects_sett)]

        if new_projects:
            settings_db.add_all(new_projects)
            settings_db.commit()

        if not settings_db.query(settings_models.Country).count():
            countries = map((lambda country: settings_models.Country(name=country.name,
                                                                     code=country.alpha_2)),
                            list(pycountry.countries))
            settings_db.add_all(countries)
            settings_db.commit()

        if not settings_db.query(settings_models.State).count():
            us_item = settings_db.query(settings_models.Country).filter_by(code='US').first()
            states = map((lambda state: settings_models.State(name=state.name,
                                                              code=state.code)),
                         list(pycountry.subdivisions.get(country_code='US')))
            us_item.states.extend(states)
            settings_db.commit()

        if not settings_db.query(settings_models.User).count():
            settings_db.add(settings_models.User(login='admin', password='1111'))
            settings_db.commit()

        return f(*args, **kwargs)

    return decorated_fun
