from datetime import datetime
from itertools import chain

from flask import request
from sqlalchemy import func

import dashboard.models.bugzilla_models as bm
from dashboard.database import bugzilla_db, settings_db
from dashboard.models.settings_models import Project


class HoursQueryMixin:
    date_fmt = "%d.%m.%Y"

    def get_hours_by_place(self, projects_ids, place_model):
        places_res = []
        places = self.get_places(place_model)
        projects = self.get_projects(projects_ids)

        for place in places:
            place_hours = sum([p.get('hours') for p in projects if p.get('id') in place.get('projects')])
            if place_hours > 0:
                place["hours"] = place_hours
                places_res.append(place)

        return projects, places_res

    def get_projects(self, projects_ids):

        if not isinstance(projects_ids, list):
            projects_ids = list(chain(*projects_ids))

        start_date, end_date = self.get_dates()
        fieldid = bm.Fielddef.query.filter(bm.Fielddef.name == 'work_time').first().id
        queryset = bugzilla_db.query(
            bm.BugsActivity, bm.Bug.product_id, bm.Product.name, func.sum(bm.BugsActivity.added)
        )
        queryset = queryset.actions(start_date, end_date, fieldid)
        actions = queryset.filter(bm.Bug.product_id.in_(projects_ids)).group_by(bm.Bug.product_id).all()
        projects = [{'id': id, 'name': name, 'hours': hours} for _, id, name, hours in actions]
        return projects

    def get_places(self, place_model):
        group_name = place_model().__class__.__name__.lower() + '_id'
        query_places = settings_db.query(func.group_concat(Project.bz_project_id.distinct()), place_model)
        query_places = query_places.join(place_model).filter(Project.enable == 1)
        query_places = query_places.group_by(getattr(Project, group_name)).all()
        places = [
            {'id': place.id,
            'name': place.name,
            'projects': [int(p) for p in projects.split(',')]}
            for projects, place in query_places
        ]
        return places

    def get_dates(self):
        start_date = datetime.strptime(request.args.get('startDate'), self.date_fmt)
        end_date = datetime.strptime(request.args.get('endDate'), self.date_fmt)
        return start_date, end_date
