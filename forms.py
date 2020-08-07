from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

def invalid_credentials(form, field):
    username_enter = form.username.data
    pass_enter = field.data

    user_obj = User.query.filter_by(username=username_enter).first()
    if user_obj is None:
        raise ValidationError("Username and Password is incorrect")
    elif pass_enter != user_obj.password:
        raise ValidationError("Username and Password is incorrect")

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)],render_kw={"placeholder": "username"})
    email = StringField('Email',validators=[DataRequired(),Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=6, max=40)])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(), invalid_credentials])
    #remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

