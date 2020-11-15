from app import app, db, encryption_engine, logger

## Plugins
from flask_login import current_user, login_user, logout_user
from flask import render_template, request, flash, redirect, url_for

## Forms
from app.forms.RegistrationForm import RegistrationForm
from app.forms.LoginForm import LoginForm
from app.forms.AddEmailForm import AddEmailForm

## Models
from app.models.User import User
from app.models.EmailAddress import EmailAddress
from app.models.PhishingEmail import PhishingEmail

## Datetime
from datetime import datetime

## Utils
from app.utils.EmailUtils import test_mailbox_conn

## Exceptions
from sqlalchemy.exc import IntegrityError


@app.route('/')
@app.route('/index')
def index():
    title = 'Home'
    project = {'project_name' : "Piscator"}
    team_members = ["Jon", "HH", "Yannis", "Joy", "CT", "Zuhree"]
    # dummy to list all users
    all_users = User.query.all()
    return render_template('index.html', title=title, project=project, team_members=team_members, all_users = all_users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    logger.debug("Entering register function")
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if request.method =='POST':
        logger.debug("Register form submitted")
        if form.validate_on_submit():
            new_user = User(username=form.username.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            logger.debug("Successfully created user %s", new_user)
            return render_template('success.html', usrname = form.username.data)
        else:
            logger.warn("Registration failed, user not registered")

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    logger.debug("Entering login function")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        logger.debug("Successfully logged in user %s", user)
        if user.is_admin:
            return redirect(url_for('admin'))
        if not user.is_admin:
            return redirect(url_for('dashboard'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    logger.debug("Successfully logged out")
    return redirect(url_for('index'))


@app.route('/admin')
def admin():
    return render_template('admin/index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = AddEmailForm()

    ## --- Add Email Form submission START ---
    if form.validate_on_submit():
        email_addr = form.email_address.data
        password = form.password.data
        # email_addr = 'piscator.fisherman@gmail.com'
        # password = 'rfdagjrrjrxfezcp'

        logger.info("Checking mailbox connectivity..")
        # Attempts a mailbox login via imap_tools based on submit
        # Adds the email address to the database
        if test_mailbox_conn(email_addr, password):
            new_email = EmailAddress()
            new_email.set_email_address(form.email_address.data)
            new_email.set_email_password(encryption_engine.encrypt(form.password.data))
            new_email.set_user_id(current_user.user_id)
            new_email.set_created_at(datetime.now())
            new_email.set_active_status(True)
            try:
                db.session.add(new_email)
                db.session.commit()
            # IntegrityError to catch existing email
            except IntegrityError:
                db.session.rollback()
                flash("Email address already exist in our database!")
                logger.error("Email already exist")
                return render_template('dashboard.html', form=form)
        # If connection to mailbox fails
        else:
            flash("Unable to connect to mailbox.")
    # -- Add Email Form submission END --
    
    return render_template('dashboard.html', current_user = current_user.username, form = form)
