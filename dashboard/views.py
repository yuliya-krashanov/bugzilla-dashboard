import calendar
import datetime
from calendar import monthrange

from flask import jsonify, render_template, request
from flask.views import View
from sqlalchemy import and_, func

import dashboard.models.bugzilla_models as bm
from dashboard import app
from dashboard.database import bugzilla_db
from dashboard.models.settings_models import Country, Project, State

from .utils import HoursQueryMixin


class IndexView(View):

    def dispatch_request(self):
        return render_template('index.html')


class ProjectsView(HoursQueryMixin, View):
    methods = ['GET']

    def dispatch_request(self):
        result = []
        projects_ids = Project.query.filter(Project.enable == 1).values("bz_project_id")
        if projects_ids:
            projects, countries_hours = self.get_hours_by_place(projects_ids, Country)
            result = {'projects': projects, 'countries': countries_hours}

        return jsonify(result)


class StatesView(HoursQueryMixin, View):
    methods = ['GET']

    def dispatch_request(self):
        result = []
        country_id = request.args.get('countryID')
        states_of_country = State.query.filter(State.country_id == country_id).all()

        if states_of_country:
            projects_ids = Project.query.filter(
                and_(Project.enable == 1, Project.country_id == country_id)
            ).values("bz_project_id")

            if projects_ids:
                _, states_hours = self.get_hours_by_place(projects_ids, State)
                result = states_hours

        return jsonify(result)


class DetailsView(View):
    methods = ['GET']
    fmt = "%m.%Y"

    def dispatch_request(self):
        data = request.args

        month = datetime.datetime.strptime(data.get('startDate'), self.fmt)
        period = data.get('period')

        start_date = {'month': month, 'year': month.replace(month=1)}.get(period)
        end_date = {
            'month': month.replace(day=monthrange(month.year, month.month)[1]),
            'year': month.replace(day=monthrange(month.year, 12)[1], month=12)
        }.get(period)

        group_func = {'month': 'day', 'year': 'month'}.get(period)

        periods_list = {
            'month': range(1, monthrange(month.year, month.month)[1] + 1), 'year': range(1, 13)
        }.get(period)

        project_id = data.get('projectID')

        fieldid = bm.Fielddef.query.filter(bm.Fielddef.name == 'work_time').first().id

        actions = bugzilla_db.query(
            bm.BugsActivity,
            getattr(func, group_func)(bm.BugsActivity.bug_when),
            func.sum(bm.BugsActivity.added)
        )
        actions = actions.actions(start_date, end_date, fieldid)
        actions = actions.filter(bm.Bug.product_id == project_id)
        actions = actions.group_by(getattr(func, group_func)(bm.BugsActivity.bug_when)).all()

        result = [
            {'name': calendar.month_name[item] if period == 'year' else item,
             'hours': sum([h for _, p, h in actions if p == item])}
            for item in periods_list
        ]
        return jsonify(result)


class Error404View:
    """
    Handle 404 errors.
    """
    @app.errorhandler(404)
    def dispatch_request(self):
        return render_template('errors/404.html'), 404


app.add_url_rule('/', view_func=IndexView.as_view('index'), endpoint="index")
app.add_url_rule('/api/projects/', view_func=ProjectsView.as_view('projects'))
app.add_url_rule('/api/states/', view_func=StatesView.as_view('states'))
app.add_url_rule('/api/details/', view_func=DetailsView.as_view('details'))
