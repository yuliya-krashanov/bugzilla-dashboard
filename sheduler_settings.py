from dashboard.jobs import update_projects


JOBS = [
    {
        'id': 'update_projects',
        'func': update_projects,
        'trigger': 'interval',
        'hours': 1
    }
]

SCHEDULER_EXECUTORS = {
    'default': {'type': 'threadpool', 'max_workers': 1}
}

SCHEDULER_JOB_DEFAULTS = {
    'coalesce': False,
    'max_instances': 1
}

SCHEDULER_API_ENABLED = True
