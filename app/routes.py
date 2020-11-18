from app import app, db, encryption_engine, logger

## Plugins
from flask_login import current_user, login_user, logout_user
from flask import render_template, request, flash, redirect, url_for

## Forms
from app.forms.RegistrationForm import RegistrationForm
from app.forms.LoginForm import LoginForm
from app.forms.AddEmailForm import AddEmailForm
from app.forms.ContactForm import ContactForm

## Models
from app.models.User import User
from app.models.EmailAddress import EmailAddress
from app.models.PhishingEmail import PhishingEmail

## Datetime
from datetime import datetime

## Utils
from app.utils.EmailUtils import test_mailbox_conn
from app.utils.EmailUtils import send_contact_us_email

## Exceptions
from sqlalchemy.exc import IntegrityError


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    contact_form = ContactForm()
    if request.method == 'POST':
        logger.debug("Email received")
        send_contact_us_email(contact_form.email_address.data, contact_form.message.data)
        return redirect(url_for('contact_form_reset'))
    return render_template('index.html', contact_form = contact_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    logger.debug("Entering register function")
    if current_user.is_authenticated:
        logger.info("User is logged in, redirecting to dashboard")
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if request.method =='POST':
        logger.debug("Register form submitted")
        if form.validate_on_submit():
            new_user = User(username=form.username.data)
            new_user.set_password(form.password.data)
            try:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('dashboard'))
            except IntegrityError:
                db.session.rollback()
                flash("Username already taken!")
                logger.error("Username already taken")
                return redirect(url_for("reg_form_reset"))
            logger.debug("Successfully created user %s", new_user)
            # return render_template('success.html', usrname = form.username.data)
        else:
            logger.warn("Registration failed, user not registered")

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
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

@app.route('/dashboard', methods=['GET'])
def dashboard():
    logger.info("Entering dashboard home..")
    if current_user.is_anonymous:
        logger.warn("Anonymous user in dashboard home, going to index..")
        return redirect(url_for('index'))
    return render_template('dashboard/dashboard_home.html')

@app.route('/dashboard/emails', methods=['GET', 'POST'])
def dash_email():
    logger.info("Entering dashboard emails..")
    # Redirects non-logged in users to index if they access dashboard from URL
    if current_user.is_anonymous:
        logger.warn("User is anonymous, redirecting to index")
        return redirect(url_for('index'))
    form = AddEmailForm()

    ## --- Add Email Form submission START ---
    if form.validate_on_submit():
        email_addr = form.email_address.data
        password = form.password.data

        logger.info("Checking mailbox connectivity..")
        # Attempts a mailbox login via imap_tools based on submit
        # Adds the email address to the database
        # -- If you want to test adding emails to a user account without checking connection
        # -- change the if statement to if True:
        # if test_mailbox_conn(email_addr, password):
        if True:
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
                return redirect(url_for('mail_form_reset'))
        # If connection to mailbox fails
        else:
            flash("Unable to connect to mailbox.")
    ## -- Add Email Form submission END --
    ## -- Default Dashboard Loading START --

    existing_emails = db.session.query(EmailAddress).filter(EmailAddress.user_id == current_user.user_id).all()
    logger.debug(existing_emails)
    return render_template('dashboard/dashboard_emails.html',
    current_user = current_user.username, form = form,
    user_emails = existing_emails)
    ## -- Default Dashboard Loading END --

@app.route('/dashboard/account', methods=['GET'])
def dash_account():
    logger.info("Entering dashboard account..")
    if current_user.is_anonymous:
        logger.warn("Anonymous user in dashboard account, going to index..")
        return redirect(url_for('index'))
    return render_template('dashboard/dashboard_account.html')

# Reroute functions to prevent form resubmission on refresh
@app.route('/mail_form_reset', methods=['GET'])
def mail_form_reset():
    logger.info("Entering function to reset form submission")
    return redirect(url_for('dashboard'))

@app.route('/reg_form_reset', methods=['GET'])
def reg_form_reset():
    logger.info("Entering function to reset form submission")
    return redirect(url_for('register'))

@app.route('/contact_form_reset', methods=['GET'])
def contact_form_reset():
    return redirect(url_for('index'))
