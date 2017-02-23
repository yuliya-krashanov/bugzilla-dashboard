from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from dashboard import app
from dashboard.database import settings_db


migrate = Migrate(app, settings_db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
