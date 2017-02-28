from sqlalchemy import and_, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query, joinedload, scoped_session, sessionmaker

from . import app


class BugzillaCustomQuery(Query):

    def actions(self, start_date, end_date, fieldid):
        from dashboard.models.bugzilla_models import BugsActivity, Bug
        queryset = self.join(BugsActivity.bug).options(joinedload('bug')).join(Bug.product)
        queryset = queryset.filter(and_(
            BugsActivity.bug_when >= start_date,
            BugsActivity.bug_when <= end_date,
            BugsActivity.fieldid == fieldid)
        )
        return queryset


bugzilla_engine = create_engine(app.config.get('BUGZILLA_DATABASE_URI', None), convert_unicode=True)
bugzilla_db = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=bugzilla_engine, query_cls=BugzillaCustomQuery)
)

settings_engine = create_engine(app.config.get('SETTINGS_DATABASE_URI', None), convert_unicode=True)
settings_db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=settings_engine))

BugzillaBase = declarative_base(bind=bugzilla_engine)
BugzillaBase.query = bugzilla_db.query_property()

SettingsBase = declarative_base(bind=settings_engine)
SettingsBase.query = settings_db.query_property()

metadata = SettingsBase.metadata


def init_db():
    metadata.create_all(bind=settings_engine)
