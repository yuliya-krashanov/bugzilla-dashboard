from flask_script import Command, prompt, prompt_pass

from dashboard.database import settings_db
from dashboard.models.bugzilla_models import Product
from dashboard.models.settings_models import Project, User


class UpdateProjectsCommand(Command):
    """Check if new projects exists in Bugzilla and add them to Settings DB"""

    def run(self):
        new_projects = []
        for product in Product.query.filter(Product.isactive == 1).all():
            if not Project.query.filter(Project.bz_project_id == product.id).count():
                new_projects.append(Project(bz_project_id=product.id, name=product.name))

        if new_projects:
            settings_db.add_all(new_projects)
            settings_db.commit()
            print('Projects was updated.')
        else:
            print('Already up-to-date.')


class CreateSuperUserCommand(Command):
    """Create new super user"""

    def run(self):

        while True:
            login = prompt('Enter username')
            if User.query.filter(User.login == login).count():
                print('User already exists, please enter another username!')
            else:
                break

        password = prompt_pass('Enter password')
        user = User(login=login, password=password)
        settings_db.add(user)
        settings_db.commit()
        print('User %s was created successfully' % login)
