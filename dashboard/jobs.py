from .commands import UpdateProjectsCommand


def update_projects():
    command = UpdateProjectsCommand()
    command.run()
