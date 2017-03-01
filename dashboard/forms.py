from werkzeug.security import check_password_hash
from wtforms import fields, form, validators

import dashboard.models.settings_models as sett_m
from dashboard.database import settings_db


class LoginForm(form.Form):
    """
    Define login and registration forms (for flask-login)
    """
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        # if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        if not check_password_hash(user.password, self.password.data):
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return settings_db.query(sett_m.User).filter_by(login=self.login.data).first()
