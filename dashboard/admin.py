from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView, expose, helpers
from flask_login import (
    LoginManager, current_user, login_required, login_user, logout_user,
)
from flask import request, redirect, url_for

from wtforms import PasswordField, ValidationError

from dashboard import app
from dashboard.database import settings_db
import dashboard.forms as forms
from dashboard.models.settings_models import Project, User


class ProtectModelView(ModelView):
    """
    Create customized model view class
    """
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('admin.login_view', next=request.url))


class ProjectModelView(ProtectModelView):
    can_create = False
    column_display_pk = False
    column_hide_backrefs = False
    column_list = ('id', 'name', 'enable', 'country', 'state', 'average_hours')
    form_excluded_columns = ('bz_project_id')


class UserModelView(ProtectModelView):

    def __init__(self, *args, **kwargs):
        super(UserModelView, self).__init__(*args, **kwargs)
        self.column_exclude_list = ('password')
        self.form_extra_fields = {'password': PasswordField('Password')}
        self.form_args = dict(login={"validators": [self.unique_login]})

    def unique_login(self, form, field):
        if User.query.filter(User.login == field.data).first():
            raise ValidationError('Login already exists')

    def on_form_prefill(self, form, id):
        form.password.data = ''

    def on_model_change(self, form, User, is_created):
        if form.password.data:
            User.set_password(form.password.data)
        else:
            del form.password


class MyAdminIndexView(AdminIndexView):
    """
    Create customized index view class that handles login & registration
    """
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = forms.LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login_user(user)

        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    @login_required
    def logout_view(self):
        user = current_user
        user.authenticated = False
        logout_user()
        return redirect(url_for('.index'))


def init_admin_login():
    # Initialize flask-login and flask-admin
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return settings_db.query(User).get(user_id)

    admin = Admin(
        app,
        name='Redwerk Bugzilla Stats',
        index_view=MyAdminIndexView(),
        template_mode='bootstrap3',
        base_template='admin/custom_base.html',
    )

    admin.add_view(UserModelView(User, settings_db))
    admin.add_view(ProjectModelView(Project, settings_db))
