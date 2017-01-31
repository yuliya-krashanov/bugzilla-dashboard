from werkzeug.security import generate_password_hash
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from dashboard.database import SettingsBase as Base

metadata = Base.metadata


class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False)
    code = Column(String(length=2))

    states = relationship('State', back_populates="country")
    projects = relationship('Project', back_populates="country")

    def __str__(self):
        return self.name


class State(Base):
    __tablename__ = 'states'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False)
    code = Column(String(length=8))
    country_id = Column(Integer, ForeignKey('countries.id', ondelete=u'CASCADE', onupdate=u'CASCADE'),
                        nullable=False, index=True)

    country = relationship('Country', back_populates="states")
    projects = relationship('Project', back_populates="state")

    def __str__(self):
        return self.name


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=150), nullable=False)
    bz_project_id = Column(Integer, nullable=False, index=True)
    country_id = Column(Integer, ForeignKey('countries.id', ondelete=u'CASCADE', onupdate=u'CASCADE'),
                        nullable=True, index=True)
    state_id = Column(Integer, ForeignKey('states.id', ondelete=u'CASCADE', onupdate=u'CASCADE'),
                      nullable=True, index=True)
    enable = Column(Boolean, nullable=False, default=True)
    country = relationship('Country', back_populates="projects")
    state = relationship('State', back_populates="projects")

    def __str__(self):
        return self.name


class User(Base):
    __tablename__ = 'users'

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.set_password(kwargs.get('password'))

    id = Column(Integer, primary_key=True)
    login = Column(String(length=50), nullable=False)
    password = Column(String(length=200), nullable=False)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Required for administrative interface
    def __str__(self):
        return self.login
