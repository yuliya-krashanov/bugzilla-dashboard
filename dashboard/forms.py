from wtforms import form, fields, validators
from werkzeug.security import generate_password_hash, check_password_hash
import dashboard.models.settings_models as sett_m
from dashboard.database import with_db


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        # if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        if check_password_hash(user.password, self.password.data):
            raise validators.ValidationError('Invalid password')

    @with_db
    def get_user(bugzilla_db, settings_db, self):
        return settings_db.query(sett_m.User).filter_by(login=self.login.data).first()
