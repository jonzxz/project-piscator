from app import app
from flask import render_template, request
from app.forms.RegistrationForm import RegistrationForm

@app.route('/')
@app.route('/index')
def index():
    title = 'Home'
    project = {'project_name' : "Piscator"}
    user = "Jon" # comment user=user for ifelse demo
    team_members = ["Jon", "HH", "Yannis", "Joy", "CT", "Zuhree"]
    return render_template('index.html', title=title, project=project, user=user, team_members=team_members)

@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)
    # form = RegistrationForm()
    # if form.validate_on_submit():
    #     new_user = User(username=form.username.data, password=)
    #db.session.add(User(username="user1", password="password1"))
