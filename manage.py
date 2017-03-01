from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from dashboard import app
from dashboard.database import settings_db
from dashboard.commands import UpdateProjectsCommand, CreateSuperUserCommand

migrate = Migrate(app, settings_db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('updateprojects', UpdateProjectsCommand)
manager.add_command('createsuperuser', CreateSuperUserCommand)


if __name__ == '__main__':
    manager.run()
