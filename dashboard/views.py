import calendar
import datetime
from calendar import monthrange

from flask import jsonify, redirect, render_template, request, url_for
from flask_admin import Admin, AdminIndexView, expose, helpers
from flask_admin.contrib.sqla import ModelView
from flask_login import (
    LoginManager, current_user, login_required, login_user, logout_user,
)
from sqlalchemy import and_, func
from wtforms import PasswordField, ValidationError

import dashboard.forms as forms
import dashboard.models.bugzilla_models as bugzilla_models
import dashboard.models.settings_models as settings_models
from dashboard import app
from dashboard.database import init_db, with_db


@app.route("/")
@init_db
def index(*args, **kwargs):
    return render_template('index.html')


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('errors/404.html'), 404


@app.route("/api/projects/", methods=['POST'])
def projects():
    projects_ids = [p.bz_project_id for p in
                    settings_models.Project.query.filter(settings_models.Project.enable == 1).all()]

    result = []
    if projects_ids:
        projects, countries_hours = get_hours_by_place(projects_ids, settings_models.Country)
        result = {'projects': projects, 'countries': countries_hours}

    return jsonify(result)


@app.route("/api/states/", methods=['POST'])
def states():
    country_id = request.get_json().get('countryID')
    result = []
    states_of_country = settings_models.State.query.filter(settings_models.State.country_id == country_id).all()

    if states_of_country:
        projects_ids = [p.bz_project_id for p in settings_models.Project.query
            .filter(and_(
                settings_models.Project.enable == 1,
                settings_models.Project.country_id == country_id))
            .all()]

        if projects_ids:
            projects, states_hours = get_hours_by_place(projects_ids, settings_models.State)
            result = states_hours

    return jsonify(result)


@with_db
def get_hours_by_place(bugzilla_db, settings_db, projects_ids, place_model):

    query_places = settings_db.query(
        func.group_concat(settings_models.Project.bz_project_id.distinct()), place_model)\
        .join(place_model).filter(settings_models.Project.enable == 1)\
        .group_by(getattr(settings_models.Project, place_model().__class__.__name__.lower() + '_id')).all()

    places = [{'id': place.id, 'name': place.name, 'projects': [int(p) for p in projects.split(',')]}
              for projects, place in query_places]

    fmt = "%d.%m.%Y"
    dates = request.get_json()
    start_date = datetime.datetime.strptime(dates.get('startDate'), fmt)
    end_date = datetime.datetime.strptime(dates.get('endDate'), fmt)

    fieldid = bugzilla_models.Fielddef.query.filter(bugzilla_models.Fielddef.name == 'work_time').first().id

    actions = bugzilla_db.query(bugzilla_models.BugsActivity, bugzilla_models.Bug.product_id,
                                bugzilla_models.Product.name,
                                func.sum(bugzilla_models.BugsActivity.added)) \
        .actions(start_date, end_date, fieldid)\
        .filter(bugzilla_models.Bug.product_id.in_(projects_ids)) \
        .group_by(bugzilla_models.Bug.product_id).all()

    projects = [{'id': id, 'name': name, 'hours': hours} for activity, id, name, hours in actions]

    for place in places:
        place_hours = sum([p.get('hours') for p in projects if p.get('id') in place.get('projects')])
        if place_hours > 0:
            place.update({'hours': place_hours})
        else:
            places.remove(place)

    return projects, places


@app.route("/api/details/", methods=['POST'])
@with_db
def details(bugzilla_db, settings_db):
    fmt = "%m.%Y"
    data = request.get_json()

    month = datetime.datetime.strptime(data.get('startDate'), fmt)
    period = data.get('period')
    start_date = {
        'month': month,
        'year': month.replace(month=1)
    }.get(period)
    end_date = {
        'month': month.replace(day=monthrange(month.year, month.month)[1]),
        'year': month.replace(day=monthrange(month.year, 12)[1], month=12)
    }.get(period)
    group_func = {
        'month': 'day',
        'year': 'month'
    }.get(period)
    periods_list = {
        'month': range(1, monthrange(month.year, month.month)[1] + 1),
        'year': range(1, 13)
    }.get(period)

    project_id = data.get('projectID')

    fieldid = bugzilla_models.Fielddef.query.filter(bugzilla_models.Fielddef.name == 'work_time').first().id

    actions = bugzilla_db.query(bugzilla_models.BugsActivity,
                                getattr(func, group_func)(bugzilla_models.BugsActivity.bug_when),
                                func.sum(bugzilla_models.BugsActivity.added)) \
        .actions(start_date, end_date, fieldid) \
        .filter(bugzilla_models.Bug.product_id == project_id) \
        .group_by(getattr(func, group_func)(bugzilla_models.BugsActivity.bug_when)).all()

    result = [
        {'label': calendar.month_name[item] if period == 'year' else item,
         'data': sum([hours for action, _period, hours in actions if _period == item])}
        for item in periods_list
    ]
    return jsonify(result)


# Create customized model view class
class ProtectModelView(ModelView):
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


def unique_login(form, field):
    if settings_models.User.query.filter(settings_models.User.login == field.data).first():
        raise ValidationError('Login already exists')


class UserModelView(ProtectModelView):
    column_exclude_list = ('password')
    form_extra_fields = {
        'password': PasswordField('Password')
    }

    form_args = dict(
        login=dict(validators=[unique_login])
    )

    def on_form_prefill(self, form, id):
        form.password.data = ''

    def on_model_change(self, form, User, is_created):
        if form.password.data:
            User.set_password(form.password.data)
        else:
            del form.password


# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):
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


# Initialize flask-login and flask-admin
@with_db
@init_db
def init_admin_login(bugzilla_db, settings_db):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return settings_db.query(settings_models.User).get(user_id)

    admin = Admin(app, name='Redwerk Bugzilla Stats', index_view=MyAdminIndexView(),
                  template_mode='bootstrap3', base_template='admin/custom_base.html')

    admin.add_view(UserModelView(settings_models.User, settings_db))
    admin.add_view(ProjectModelView(settings_models.Project, settings_db))


init_admin_login()
