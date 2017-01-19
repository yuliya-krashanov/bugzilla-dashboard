import calendar
import datetime
from calendar import monthrange

from flask import redirect, url_for
from flask import render_template, jsonify, request
from flask_admin import Admin, AdminIndexView, helpers, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_user, logout_user
from wtforms import PasswordField
from sqlalchemy import func
from sqlalchemy.orm import joinedload

import dashboard.forms as forms
import dashboard.models.settings_models as sett_m
import dashboard.models.bugzilla_models as bugz_m
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
    projects_ids = [p.bz_project_id for p in sett_m.Project.query.filter(sett_m.Project.enable == 1).all()]

    result = []
    if projects_ids:
        projects, countries_hours = get_hours_by_place(projects_ids, sett_m.Country)
        result = {'projects': projects, 'countries': countries_hours}

    return jsonify(result)


@app.route("/api/states/", methods=['POST'])
def states():
    state_id = request.get_json().get('stateID')

    projects_ids = [p.bz_project_id for p in sett_m.Project.query.filter(sett_m.Project.enable == 1)
                    .filter(sett_m.Project.state_id == state_id).all()]

    result = []
    if projects_ids:
        projects, states_hours = get_hours_by_place(projects_ids, sett_m.State)
        result = states_hours

    return jsonify(result)


@with_db
def get_hours_by_place(bugzilla_db, settings_db, projects_ids, place_model):

    places = [{'id': place.id, 'name': place.name, 'projects': [int(p) for p in projects.split(',')]}
                 for projects, place in settings_db.query(func.group_concat(sett_m.Project.bz_project_id.distinct()),
                                                          place_model).join(place_model)
                    .filter(sett_m.Project.enable == 1).group_by(sett_m.Project.country_id).all()]

    fmt = "%d.%m.%Y"
    dates = request.get_json()
    start_date = datetime.datetime.strptime(dates.get('startDate'), fmt)
    end_date = datetime.datetime.strptime(dates.get('endDate'), fmt)

    # TODO: delete hardcoded fieldid
    actions = bugzilla_db.query(bugz_m.BugsActivity, bugz_m.Bug.product_id, bugz_m.Product.name,
                                func.sum(bugz_m.BugsActivity.added)) \
        .join(bugz_m.BugsActivity.bug).options(joinedload('bug')).join(bugz_m.Bug.product) \
        .filter(bugz_m.Bug.product_id.in_(projects_ids)) \
        .filter(bugz_m.BugsActivity.bug_when >= start_date).filter(bugz_m.BugsActivity.bug_when <= end_date) \
        .filter(bugz_m.BugsActivity.fieldid == 50).group_by(bugz_m.Bug.product_id).all()

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
            'month': range(1, monthrange(month.year, month.month)[1]+1),
            'year': range(1, 13)
        }.get(period)

    project_id = data.get('projectID')

    actions = bugzilla_db.query(bugz_m.BugsActivity, getattr(func, group_func)(bugz_m.BugsActivity.bug_when),
                                func.sum(bugz_m.BugsActivity.added)) \
        .join(bugz_m.BugsActivity.bug).options(joinedload('bug')).join(bugz_m.Bug.product) \
        .filter(bugz_m.Bug.product_id == project_id) \
        .filter(bugz_m.BugsActivity.bug_when >= start_date).filter(bugz_m.BugsActivity.bug_when <= end_date) \
        .filter(bugz_m.BugsActivity.fieldid == 50).group_by(getattr(func, group_func)(bugz_m.BugsActivity.bug_when)).all()

    result = [{'label': calendar.month_name[item] if period == 'year' else item,
            'data': sum([hours for action, period, hours in actions if period == item])} for item in periods_list]
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
    column_list = ('id', 'name', 'enable', 'country')
    form_excluded_columns = ('bz_project_id')


class UserModelView(ProtectModelView):
    column_exclude_list = ('password')
    form_extra_fields = {
        'password': PasswordField('Password')
    }


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
    def logout_view(self):
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
        return settings_db.query(sett_m.User).get(user_id)

    admin = Admin(app, name='Redwerk Bugzilla Stats', index_view=MyAdminIndexView(),
                  template_mode='bootstrap3', base_template='admin/custom_base.html')

    admin.add_view(UserModelView(sett_m.User, settings_db))
    admin.add_view(ProjectModelView(sett_m.Project, settings_db))


init_admin_login()

