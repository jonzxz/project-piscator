from app import app, db
from flask import render_template, request, flash, redirect, url_for
from app.forms.RegistrationForm import RegistrationForm
from app.models.User import User
from app.models.EmailAddress import EmailAddress

@app.route('/')
@app.route('/index')
def index():
    title = 'Home'
    project = {'project_name' : "Piscator"}
    user = None
    team_members = ["Jon", "HH", "Yannis", "Joy", "CT", "Zuhree"]
    return render_template('index.html', title=title, project=project, user=user, team_members=team_members)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return render_template('success.html', usrname = form.username.data)

    return render_template('register.html', form=form)


@app.route('/makeuser')
def dummy_add_user():
    usrname = "User1"
    password = "password1"
    new_user = User(username=usrname, password=password)
    db.session.add(new_user)
    db.session.commit()
    return render_template('success.html', usrname = usrname)
