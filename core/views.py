from flask import (
    render_template,
    redirect, request,
    flash, session,
    jsonify
)

from utils.forms import (
    LoginForm, SignUpForm,
    AddTaskForm, AddProjectForm,
    ChangeEmailForm, ChangePasswordForm, SortTaskForm
)
from core import core
from app import api
from flask_restful import reqparse, Resource
from utils.decorators import login_required
from flask import Markup
import utils.functions as functions
from datetime import datetime, date

parser = reqparse.RequestParser()


@core.route('/')
def home_page():
    '''
        App for hompage
    '''
    session['user_count'] = functions.get_user_count()
    try:
        if session['username']:
            return render_template('homepage.html', username=session['username'])
        return render_template('homepage.html')
    except (KeyError, ValueError):
        return render_template('homepage.html')


@core.route('/tasks/', methods=('GET', 'POST'))
@login_required
def tasks():
    '''
        App for task list
    '''
    form = SortTaskForm()
    tasks = functions.get_data_using_user_id(session['id'])
    return render_template('view_tasks.html', form=form, tasks=tasks, username=session['username'])


@core.route('/login/', methods=('GET', 'POST'))
def login():
    '''
        App for creating Login page
    '''
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = functions.generate_password_hash(request.form['password'])
        user_id = functions.check_user_exists(username, password)
        if user_id:
            session['username'] = username
            session['id'] = user_id
            functions.store_last_login(session['id'])
            return redirect('/')
        else:
            flash('Username/Password Incorrect!')
    return render_template('login.html', form=form)


@core.route('/signup/', methods=('GET', 'POST'))
def signup():
    '''
        App for registering new user
    '''
    form = SignUpForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = functions.generate_password_hash(request.form['password'])
        email = request.form['email']
        check = functions.check_username(username)
        if check:
            flash('Username already taken!')
        else:
            functions.signup_user(username, password, email)
            session['username'] = username
            user_id = functions.check_user_exists(username, password)
            session['id'] = user_id
            return redirect('/')
    return render_template('signup.html', form=form)


@core.route("/logout/")
def logout():
    '''
        App for logging out user
    '''
    session['username'] = None
    session['id'] = None
    return login()


def validate_enddate_field(field):
    """
        Helper function that checks the validity of the deadline
    """
    if not field:
        return True
    today = date.today()
    ntoday = today.strftime("%Y-%m-%d")
    data1 = ntoday.split("-")
    data2 = field.split("-")
    for i in range(3):
        if int(data1[i]) < int(data2[i]):
            return True
    return False


@core.route("/tasks/add/", methods=('GET', 'POST'))
@login_required
def add_task():
    '''
        App for adding task
    '''
    form = AddTaskForm()
    if form.validate_on_submit():
        task_name = request.form.get('name')
        project_name = request.form.get('project_name', None)
        status = 0
        deadline = request.form.get('deadline')
        priority = int(request.form.get('priority'))
        user_id = session['id']
        if not validate_enddate_field(deadline):
            flash(u"deadline date must not be earlier than today date.", "error")
        elif not project_name:
            functions.add_task(task_name, None, status, deadline, priority, user_id)
            flash(u"Task was successfully added", "success")
        else:
            flag = True
            for pr in functions.get_all_projects(user_id):
                if pr[1] == project_name:
                    functions.add_task(task_name, pr[0], status, deadline, priority, user_id)
                    flag = False
                    break
            if not flag:
                flash(u"Task was successfully added", "success")
            else:
                flash(u"such project doesn't exist", "error")
    return render_template('add_task.html', form=form, username=session['username'])


@core.route("/tasks/edit/<tsk_id>/", methods=('GET', 'POST'))
@login_required
def edit_task(tsk_id):
    '''
        App for editing a specific task
    '''
    tsk_id = int(tsk_id)
    form = AddTaskForm()
    form.submit.label.text = "edit task"
    if request.method == 'GET':
        data = functions.get_data_using_id(tsk_id)
        form.task_id.data = tsk_id
        form.name.data = data[1]
        if data[4]:
            form.deadline.data = datetime.strptime(data[4], "%Y-%m-%d")
        form.project_name.data = functions.get_data_using_project_id(data[2])[0] if data[2] else ""
        form.priority.data = data[5]
        return render_template('edit_task.html', form=form, username=session['username'], id=tsk_id)
    elif form.validate_on_submit():
        name = request.form['name']
        project_name = request.form.get('project_name', None)
        deadline = request.form.get('deadline', None)
        priority = int(request.form.get('priority'))
        user_id = session['id']
        flag = True
        status=None
        if not validate_enddate_field(deadline):
            flash(u"deadline date must not be earlier than today date.", "error")
        elif not project_name:
            functions.edit_task(name, project_name, status, deadline, priority, tsk_id)
            flag = False
        else:
            for pr in functions.get_all_projects(user_id):
                if pr[1] == project_name:
                    flag = False
                    functions.edit_task(name, pr[0], status, deadline, priority, tsk_id)
            if flag:
                flash(u"such project doesn't exist", "error")
        if not flag:
            return redirect("/tasks/")
    return render_template('edit_task.html', form=form, username=session['username'], id=tsk_id)


@core.route("/tasks/sort/", methods=('GET', 'POST'))
@login_required
def sort_tasks():
    '''
        App for filtering tasks
    '''
    form = SortTaskForm()
    res = []
    status = request.form.get('status')
    deadline = request.form.get('deadline')
    project_name = request.form.get('project_name')
    priority = request.form.get('priority')
    user_id = session['id']
    project = None
    if project_name:
        for pr in functions.get_all_projects(user_id):
            if pr[1] == project_name:
                project = pr[0]
                break
    tasks= functions.get_data_using_user_id(user_id)
    for task in tasks:
        if task[3] and 'completed'== status or  'uncompleted'== status and not task[3] or status=='':
            if (priority and int(priority) == task[5]) or not priority:
                if (deadline and deadline == task[4]) or not deadline:
                    if project and int(project) == task[2]  or not project_name:
                        res.append(task)
    return render_template('view_tasks.html', form=form, tasks=res, username=session['username'])

@core.route("/tasks/cancel/", methods=('GET', 'POST'))
@login_required
def cancel():
    '''
        App for cancel filtering tasks
    '''
    form = SortTaskForm()
    form.status.data = ""
    form.deadline=""
    form.project_name.data = ""
    form.priority.data = ""
    return redirect("/tasks/")


@core.route("/tasks/status/<tsk_id>/", methods=('GET', 'POST'))
@login_required
def task_status(tsk_id):
    '''
        App for change task status
    '''
    form=SortTaskForm()
    task = functions.get_data_using_id(tsk_id)
    functions.edit_task(task[1], task[2], (task[3] + 1) % 2, task[4], task[5], task[0])
    tasks= functions.get_data_using_user_id(session['id'])
    return render_template('view_tasks.html', form=form, tasks=tasks, username=session['username'], id=tsk_id)


@core.route("/tasks/delete/<id>/", methods=['GET', 'POST'])
@login_required
def delete_task(id):
    '''
        App for deleting task
    '''
    functions.delete_task_using_id(id)
    tsk = functions.get_data_using_user_id(session['id'])
    tasks = []
    if tsk:
        for t in tsk:
            tasks.append(t)
    return redirect("/tasks/")


@core.route("/projects/add/", methods=['GET', 'POST'])
@login_required
def add_project():
    '''
        App for adding a project
    '''
    form = AddProjectForm()
    if form.validate_on_submit():
        project = request.form['name']
        functions.add_project(project, session['id'])
        flash("Project was successfully added")
    return render_template('add_project.html', form=form, username=session['username'])


@core.route("/projects/")
@login_required
def view_projects():
    '''
          App for updating data a specific project
    '''
    projects = functions.get_all_projects(session['id'])
    return render_template('view_projects.html', projects=projects, username=session['username'])


@core.route("/projects/edit/<pr_id>/", methods=('GET', 'POST'))
@login_required
def edit_project(pr_id):
    '''
        App for updating data a specific project
    '''
    pr_id = int(pr_id)
    form = AddProjectForm()
    if request.method == 'GET':
        data = functions.get_data_using_project_id(pr_id)
        form.name.data = data[0]
        form.submit.label.text = "edit project"
        return render_template('edit_project.html', form=form, username=session['username'], id=pr_id)
    elif form.validate_on_submit():
        project_name = request.form['name']
        functions.edit_project(project_name, pr_id)
        return redirect("/projects/")
    return render_template('edit_project.html', form=form, username=session['username'], id=pr_id)


@core.route("/projects/delete/<pr_id>/")
@login_required
def delete_project(pr_id):
    '''
        App for deleting a specific project
    '''
    functions.delete_project_using_id(int(pr_id))
    return redirect("/projects/")


@core.route("/settings/")
@login_required
def profile_settings():
    '''
        App for getting profile settings for a user
    '''
    user_data = functions.get_user_data(session['id'])
    task_count = functions.get_number_of_tasks(session['id'])
    project_count = functions.get_number_of_projects(session['id'])
    return render_template(
        'profile_settings.html',
        user_data=user_data,
        username=session['username'],
        task_count=task_count,
        project_count=project_count
    )


@core.route("/settings/change_email/", methods=['GET', 'POST'])
@login_required
def change_email():
    '''
        App for changing the email of a user
    '''
    form = ChangeEmailForm()
    if form.validate_on_submit():
        email = request.form['email']
        functions.edit_email(email, session['id'])
        return redirect('/settings/')
    return render_template('change_email.html', form=form, username=session['username'])


@core.route("/settings/change_password/", methods=['GET', 'POST'])
@login_required
def change_password():
    '''
        App for changing the password of a user
    '''
    form = ChangePasswordForm()
    if form.validate_on_submit():
        password = request.form['password']
        functions.edit_password(password, session['id'])
        return redirect('/settings/')
    return render_template('change_password.html', form=form, username=session['username'])


@core.route('/background_process/')
def background_process():
    '''
        App for handling AJAX request for searching tasks
    '''
    try:
        tasks = request.args.get('tasks')
        if tasks == '':
            return jsonify(result='')
        results = functions.get_search_data(str(tasks), session['id'])
        temp = ''
        for result in results:
            temp += "<h4><a href='/tasks/" + str(result[0]) + "/'>" + result[1] + "</a></h4><br>"
        return jsonify(result=Markup(temp))
    except Exception as e:
        return str(e)


class GetDataUsingUserID(Resource):
    def post(self):
        try:
            args = parser.parse_args()
            username = args['username']
            password = functions.generate_password_hash(args['password'])
            user_id = functions.check_user_exists(username, password)
            if user_id:
                functions.store_last_login(user_id)
                return functions.get_rest_data_using_user_id(user_id)
            else:
                return {'error': 'You cannot access this page, please check username and password'}
        except AttributeError:
            return {'error': 'Please specify username and password'}


api.add_resource(GetDataUsingUserID, '/api/')
parser.add_argument('username')
parser.add_argument('password')
