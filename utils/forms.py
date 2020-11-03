from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, IntegerField, HiddenField, SelectField
from wtforms import validators
from wtforms.fields.html5 import DateField



class LoginForm(FlaskForm):
    username = TextField('Username*', [validators.data_required("Please enter \
      your name.")])
    password = PasswordField('Password*', [validators.data_required("Please enter \
      your password.")])
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):
    username = TextField('Username*', [validators.data_required("Please enter \
      your username")])
    email = TextField('Email*', [validators.data_required("Please enter \
      your email"), validators.Email('Email format incorrect')])
    password = PasswordField('Password*', [validators.data_required("Please enter \
      your password"), validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password*', [validators.data_required("Confirm \
      your password")])
    submit = SubmitField('Signup')


class AddTaskForm(FlaskForm):
    task_id = HiddenField("TASK ID:")
    name = TextField('Task*:', [validators.data_required("Please enter valid task name.")])
    deadline=DateField('Deadline:',format="%Y-%m-%d",validators=(validators.Optional(),))
    project_name= TextField('Project:')
    priority=SelectField("Priority", choices=[("1","1"),("2","2"),("3","3")])
    submit = SubmitField('Add task')

class SortTaskForm(FlaskForm):
    status = SelectField("Status:", choices=[('',''),("completed","completed"),("uncompleted","uncompleted")])
    deadline = DateField('Deadline:', format="%Y-%m-%d", validators=(validators.Optional(),))
    priority=SelectField("Priority:", choices=[("",""),("1","1"),("2","2"),("3","3")])
    project_name= TextField('Project:')
    submit = SubmitField('Save')


class AddProjectForm(FlaskForm):
    name = TextField('Name* :', [validators.data_required("Please enter valid  project name")])
    submit = SubmitField('Add project')


class ChangeEmailForm(FlaskForm):
    email = TextField('Email*', [validators.data_required("Please enter \
      your email"), validators.Email('Email format incorrect')])
    submit = SubmitField('Update Email')


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password*', [validators.data_required("Please enter \
      your password"), validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password*', [validators.data_required("Confirm \
      your password")])
    submit = SubmitField('Update Password')
