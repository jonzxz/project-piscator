from app import app, db, logger, model
## Plugins
from flask_login import current_user, login_user, logout_user
from flask import render_template, request, flash, redirect, url_for, session

## Forms
from app.forms.RegistrationForm import RegistrationForm
from app.forms.LoginForm import LoginForm
from app.forms.AddEmailForm import AddEmailForm
from app.forms.ChangeEmailPasswordForm import ChangeEmailPasswordForm
from app.forms.ContactForm import ContactForm
from app.forms.AccountSettingsForm import AccountSettingsForm
from app.forms.DisableAccountForm import DisableAccountForm
from app.forms.ResetPasswordRequestForm import ResetPasswordRequestForm
from app.forms.UpdatePasswordForm import UpdatePasswordForm

## Models
from app.models.User import User
from app.models.EmailAddress import EmailAddress
from app.models.PhishingEmail import PhishingEmail

## Datetime
from datetime import datetime, date, timedelta
from pytz import timezone

## Utils
from app.utils.EmailUtils import test_mailbox_conn
from app.utils.EmailUtils import send_contact_us_email
from app.utils.EmailUtils import get_imap_svr
from app.utils.EmailUtils import send_phish_check_notice
from app.utils.EmailUtils import send_password_token
from app.utils.EmailUtils import check_valid_time
from app.utils.EmailUtils import check_valid_sender
from app.utils.DBUtils import get_user_by_id
from app.utils.DBUtils import get_user_by_name
from app.utils.DBUtils import get_email_address_by_address
from app.utils.DBUtils import get_email_address_by_email_id
from app.utils.DBUtils import get_existing_addresses_by_user_id
from app.utils.DBUtils import get_owner_id_from_email_id
from app.utils.DBUtils import check_p_mail_exist
from app.utils.DBUtils import get_homepage_stats
from app.utils.DBUtils import get_admin_dashboard_stats
from app.utils.DBUtils import get_admin_monthly_overview
from app.utils.DBUtils import get_user_dashboard_stats
from app.utils.DBUtils import get_user_monthly_overview
from app.utils.DBUtils import disable_emails_by_user_id

## Exceptions
from sqlalchemy.exc import IntegrityError

# Mailbox
from imap_tools import MailBox, AND, OR
from app.models.Mail import Mail
from app.machine_learning.EmailData import EmailData

# Email
from email.errors import HeaderParseError

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    statistics = get_homepage_stats()
    contact_form = ContactForm()
    if request.method == 'POST':
        logger.info("Contact Us Form sent")
        send_contact_us_email(contact_form.email_address.data\
        , contact_form.message.data)
        return redirect(url_for('index'))
    return render_template('index.html', contact_form = contact_form\
    , statistics=statistics)

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
            user_exist = get_user_by_name(form.username.data)
            if user_exist == None:
                new_user = User(username=form.username.data)
                new_user.set_password(form.password.data)
                new_user.set_last_logged_in(datetime.now())
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                session["user_id"] = new_user.get_id()
                session["username"] = new_user.get_username()
                logger.debug("Successfully created user %s", new_user)
                return redirect(url_for('dashboard'))
            else:
                flash("Username already taken!")
                logger.error("Username already taken")
                logger.warning("Registration failed, user not registered")
                return redirect(url_for("register"))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    logger.debug("Entering login function")
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_name(form.username.data)

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

        if user.get_active_status() == False:
            flash('Account is disabled, contact support!', 'error')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        user.set_last_logged_in(datetime.now())
        db.session.commit()
        session["user_id"] = user.get_id()
        session["username"] = user.get_username()
        logger.debug("Successfully logged in user %s", user)

        return redirect(url_for('admin.index'))\
        if user.get_admin_status() == True else redirect(url_for('dashboard'))

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    logger.info("Logging out user, removing credentials from session")
    session.pop('user_id', None)
    session.pop('username', None)
    logger.debug("Successfully logged out")
    return redirect(url_for('index'))

@app.route('/admin')
@app.route('/admin/')
def admin():
    logger.info("Entering admin route")
    if current_user.get_admin_status() == True:
        logger.info("Admin user logging in, redirecting to admin portal")

        statistics = get_admin_dashboard_stats()
        monthly_stats = get_admin_monthly_overview()

        return render_template('admin/index.html', statistics = statistics \
        , monthly_stats = monthly_stats)
    else:
        logger.warn("Normal user accessing admin, redirecting to dashboard")
        return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    logger.info("Entering dashboard home..")
    if current_user.is_anonymous:
        logger.warning("Anonymous user in dashboard home, going to index..")
        return redirect(url_for('index'))
    if current_user.get_admin_status() == True:
        logger.info("Admin logging in, redirecting to admin portal")
        return redirect(url_for('admin.index'))

    logger.info("User logging in, redirecting to users portal")

    statistics = get_user_dashboard_stats()
    monthly_stats = get_user_monthly_overview()

    return render_template('dashboard/dashboard_home.html', \
    statistics = statistics, monthly_stats = monthly_stats)

@app.route('/dashboard/emails', methods=['GET', 'POST'])
def dash_email():
    logger.info("Entering dashboard emails..")
    # Redirects non-logged in users to index if they access dashboard from URL
    if current_user.is_anonymous:
        logger.warning("User is anonymous, redirecting to index")
        return redirect(url_for('index'))

    add_email_form = AddEmailForm()
    change_email_password_form = ChangeEmailPasswordForm()
    existing_addresses = get_existing_addresses_by_user_id(current_user.user_id)
    return render_template('dashboard/dashboard_emails.html',
    current_user = current_user.username, add_email_form = add_email_form, \
    change_email_password_form = change_email_password_form, \
    user_emails = existing_addresses)
    ## -- Default Dashboard Loading END --

@app.route('/dashboard/add_email', methods=['POST'])
def add_email():
    logger.info("Entering add_email..")
    add_email_form = AddEmailForm()
    change_email_password_form = ChangeEmailPasswordForm()
    existing_addresses = get_existing_addresses_by_user_id(current_user.user_id)

    ## --- Add Email Form submission START ---
    if add_email_form.validate_on_submit():
        email_addr = add_email_form.email_address.data
        password = add_email_form.password.data

        # Checks if email already exist in database
        email_exist = get_email_address_by_address(email_addr)

        if email_exist == None:
            # Attempts a mailbox login via imap_tools based on submit
            # Adds the email address to the database
            logger.info("Checking mailbox connectivity..")
            # -- If you want to test adding emails to a user account
            # -- without checking connection
            # -- change the if statement to if True:
            if test_mailbox_conn(email_addr, password):
                new_email = EmailAddress()
                new_email.set_email_address(add_email_form.email_address.data)
                new_email.set_email_password(add_email_form.password.data)
                new_email.set_owner_id(current_user.user_id)
                new_email.set_created_at(datetime.now())
                new_email.set_active_status(True)
                db.session.add(new_email)
                db.session.commit()
            # If connection to mailbox fails
            else:
                flash("Unable to connect to mailbox."\
                " Maybe you've entered a wrong email/password?", 'error')
        else:
            flash("{} already exist in our database!".format(email_addr), 'error')
            logger.error("Email already exist")
    else:
        if not add_email_form.email_address.data:
            logger.warn('Empty email submitted')
            flash('Email Address cannot be empty!', 'error')
        if not add_email_form.password.data:
            logger.warn('Empty password submitted')
            flash('Password cannot be empty!', 'error')
    ## -- Add Email Form submission END --

    return redirect(url_for('dash_email'))

@app.route('/dashboard/update_email_password', methods=['POST'])
def update_email_password():
    logger.info("Entering update_email_password..")
    add_email_form = AddEmailForm()
    change_email_password_form = ChangeEmailPasswordForm()
    existing_addresses = get_existing_addresses_by_user_id(current_user.user_id)

    # -- Update Email Password submission START
    if change_email_password_form.is_submitted():
        logger.info("Address: %s", change_email_password_form.email_address.data)
        email_addr = change_email_password_form.email_address.data
        email_address = get_email_address_by_address(email_addr)

        logger.info("Entering password change")
        if email_address is not None and email_address.get_active_status():
            if change_email_password_form.new_password.data:
                if test_mailbox_conn(email_addr\
                , change_email_password_form.new_password.data):
                    flash('Password successfully updated!', 'success')
                    email_address.set_email_password(\
                    change_email_password_form.new_password.data)
                    db.session.commit()
                else:
                    flash('Unable to connect to mailbox with new password!', 'error')
            else:
                logger.info("Password entered is empty.")
                flash('Password cannot be empty!.', 'error')
        else:
                logger.warn("Email address is inactive or None.")
                flash('Email address is inactive or does not exist', 'error')
        # -- Update Email Password submission END --

    return redirect(url_for('dash_email'))

@app.route('/dashboard/account', methods=['GET', 'POST'])
def dash_account():
    logger.info("Entering dashboard account..")
    if current_user.is_anonymous:
        logger.warning("Anonymous user in dashboard account, going to index..")
        return redirect(url_for('index'))

    password_form = AccountSettingsForm()
    disable_form = DisableAccountForm()
    user = get_user_by_id(current_user.user_id)
    status = user.get_active_status()

    return render_template('dashboard/dashboard_account.html',\
    current_user = current_user, password_form = password_form,\
    disable_form = disable_form, status = status)

@app.route('/dashboard/account/update_password', methods=['POST'])
def update_password():
    logger.info("Entering update_password")
    password_form = AccountSettingsForm()
    disable_form = DisableAccountForm()
    user = get_user_by_id(current_user.user_id)

    # 1st Condition: valid password + new passwords are valid and NOT empty
    # 2nd Condition: invalid current password
    # 3rd Condition: empty new password
    # 4th Condition: mismatced new passwords
    # Code is handled this way due to method being rerouted from dash_account
    # so the validators in the form do not work, thus requiring manual handling
    if password_form.is_submitted():
        logger.info("Password update form submitted")
        if user.check_password(password_form.current_password.data) and \
        not (password_form.new_password.data == '' \
        or password_form.confirm_new_password.data == '') and \
        password_form.new_password.data == \
        password_form.confirm_new_password.data:
            logger.info("All fields entered are valid")
            user.set_password(password_form.new_password.data)
            flash('Password Successfully Changed!', 'success')
            db.session.commit()
            logger.debug("Successfully changed user %s password"\
            ", updated database", user)

        elif not user.check_password(password_form.current_password.data):
            logger.info("Wrong current password entered")
            flash('Invalid Current Password!', 'error')
        elif password_form.new_password.data == '' or \
        password_form.confirm_new_password.data == '':
            logger.info("Either password submitted is empty")
            flash('Passwords cannot be empty!', 'error')
        elif not password_form.new_password.data \
        == password_form.confirm_new_password.data:
            logger.info("Mismatched new passwords entered")
            flash('New Password and Confirm New Password must match!', 'error')

    return redirect(url_for('dash_account'))

@app.route('/dashboard/account/disable', methods=['POST'])
def disable_account():
    logger.info("Entering disable_account")
    password_form = AccountSettingsForm()
    disable_form = DisableAccountForm()
    user = get_user_by_id(current_user.user_id)

    # 1st Condition: valid password + slider is enabled
    # 2nd Condition: invalid current password
    # 3rd Condition: slider not turned on
    # Code is handled this way due to method being rerouted from dash_account
    # so the validators in the form do not work, thus requiring manual handling
    if disable_form.is_submitted():
        slider_data = request.form.get('disable_account')

        logger.info("Disable account form submitted")

        if user.check_password(disable_form.current_password.data) and \
        slider_data == 'on':
            logger.info("all good!")
            user.set_active_status(False)
            disable_emails_by_user_id(user.get_id())
            db.session.commit()
            flash('Account is Disabled! You\'ll be logged out in 5 seconds..',\
             'error')
        elif not user.check_password(disable_form.current_password.data):
            logger.info("Wrong password entered")
            flash('Invalid Current Password!', 'error')
        elif not slider_data == 'on':
            logger.info('Slider not turned on')
            flash('If you intend to disable your account, click the slider!', 'error')

    return redirect(url_for('dash_account'))

@app.route('/dashboard/emails/phish/<mid>')
def check_phish(mid):
    phishing_mails = []

    # Retrieves the email address instance
    logger.info("Click-to-check entered..")

    owner_id = get_owner_id_from_email_id(mid)
    if current_user.is_anonymous or not owner_id == current_user.get_id() :
        logger.warning("Anonymous or unauthorized user attempting"\
        " phish check of address ID {}!".format(mid))
        return redirect(url_for('index'))

    mailaddr = get_email_address_by_email_id(mid)

    # Redirects back to page if selected email is inactive
    if mailaddr.get_active_status() == False:
        logger.warning("Redirecting.. User selected inactive email address %s"\
        , mailaddr.get_email_address())
        flash("Email is inactive!", 'error')
        return redirect(url_for('dash_email'))

    logger.info("Mailbox selected is %s", mailaddr.get_email_address())

    try:
        # Logs in to mailbox by retrieving the corresponding IMAP server
        imap_svr = get_imap_svr(mailaddr.get_email_address())
        logger.info("Retrieving IMAP server: %s", imap_svr)
        mailbox = MailBox(imap_svr)
        logger.info("Attempting connection..")
        mailbox.login(mailaddr.get_email_address()\
        , mailaddr.get_decrypted_email_password())
        logger.info("Connected to mailbox %s", mailaddr.get_email_address())
    except ConnectionRefusedError:
        logger.error("Unable to connect to mailbox for %s", mailaddr.get_email_address())
        flash("Unable to connect to mailbox, please update your password!", 'error')
        return redirect(url_for('dash_email'))

    # Retrieves date last updated
    # if new email address is added column is empty
    # sets last_updated to today - 1 day so that mails in the last 24 hours
    # are checked
    last_updated = mailaddr.get_last_updated() \
    if mailaddr.get_last_updated() else datetime.today() - timedelta(days=1)


    # Selects mailbox to Inbox only
    mailbox.folder.set("INBOX")
    logger.info("Fetching mails..")

    # Sets a check criteria so that
    # only mails newer than last_updated and unread mails are checked
    check_criteria = AND(date_gte=last_updated.date(), seen=False)

    """
    FOR DEMO USE
    """
    # Test code to intentionally pull retrieve backdated emails for demo purposes
    # last_updated = datetime(2020, 12,17, 0, 0, 0)
    # check_criteria = AND(date_gte=[date(2020, 12, 17)], seen=False)

    # Fetch mails from mailbox based on criteria, does not "read" the mail
    # and retrieves in bulk for faster performance at higher computing cost
    all_mails = mailbox.fetch(check_criteria, reverse=True, mark_seen=False, bulk=True)

    logger.info("Mails fetched..")

    # Iterates through the mails that are not sent from the sender's address
    # Creates a EmailData instance for each mail to generate features based on
    # preprocessing logic, passes it into the model - if predict returns 1 it is a detected phish
    # appends the detected mail into a list of Mail (phishing_mails)
    # The purpose of Mail class is for easier display - the values are pulled from the
    # imap_tool's Mail item instead of our EmailData.
    # Inserts all phishing mails to the database
    data = {
        'total_count' : 0,
        'detection_count' : 0,
        'check_time' : datetime.now().strftime('%d-%m-%Y, %H:%M')
    }

    mail_check_count = 0

    for msg in all_mails:
        try:
            sender = msg.from_
        except HeaderParseError:
            # Exception happens when a msg.from_ is malformed resulting in
            # unparseable values. Automatically assume phishing email and add to record.
            # Denote Sender as 'INVALID_SENDER'
            logger.error("HeaderParseError, unparseable msg.from_. \
            Setting sender as INVALID_SENDER")
            sender = 'INVALID_SENDER'
        if (check_valid_time(last_updated, msg.date)) \
        and check_valid_sender(sender, mailaddr.get_email_address()):
            data['total_count']+=1
            mail_check_count +=1
            mail_item = EmailData(msg.subject, sender, msg.attachments\
            , (msg.text + msg.html), msg.headers)
            mail_item.generate_features()
            result = model.predict(mail_item.repr_in_arr())
            logger.info("Checking mail: %s -- Result: %s"\
            , mail_item.get_subject(), result)
            if result == 1:
                logger.info("Phishing mail detected, subject: %s", msg.subject)

                mail_exist = check_p_mail_exist(mailaddr.get_email_id()\
                , msg.subject, mail_item.get_content())

                if not mail_exist:
                    phishing_mails.append(Mail(sender, \
                    msg.date.astimezone(timezone('Asia/Singapore')), msg.subject))
                    data['detection_count']+=1
                    detected_mail = PhishingEmail( \
                    sender_address = sender, \
                    subject = msg.subject, \
                    content = mail_item.get_content(), \
                    created_at = datetime.now(), \
                    receiver_id = mailaddr.get_email_id()
                    )
                    db.session.add(detected_mail)

    # Updates last updated to current time
    mailaddr.set_last_updated(datetime.now())
    logger.info("Updating mailbox last updated from %s to %s",\
    last_updated.strftime("%d-%m-%Y, %H:%M:%S"), datetime.now())

    mailaddr.set_phishing_mail_detected(data['detection_count'])
    mailaddr.set_total_mails_checked(mail_check_count)
    db.session.commit()
    logger.info("Finished checking mails.. logging out")
    mailbox.logout()
    send_phish_check_notice(mailaddr.get_email_address(), phishing_mails)

    mailaddr = get_email_address_by_email_id(mid)
    mail_address = mailaddr.get_email_address()

    # return redirect(url_for('dashboard'))
    return render_template('dashboard/detection_results.html', \
    phishing_mails = phishing_mails, data=data, mail_address = mail_address)

@app.route('/dashboard/emails/activation/<mid>')
def mail_activation(mid):
    owner_id = get_owner_id_from_email_id(mid)

    if current_user.is_anonymous or not owner_id == current_user.get_id() :
        logger.warning("Anonymous or unauthorized user "\
        "attempting activation of address ID {}!".format(mid))
        return redirect(url_for('index'))

    logger.info("Entering function to enable/disable email..")
    mailaddr = get_email_address_by_email_id(mid)
    if mailaddr.get_active_status() == True:
        mailaddr.set_active_status(False)
        mailaddr.set_notification_pref(False)
    else:
        mailaddr.set_active_status(True)
    db.session.commit()
    return redirect(url_for('dash_email'))

@app.route('/dashboard/emails/notif/<mid>')
def mail_notification_preference(mid):
    owner_id = get_owner_id_from_email_id(mid)

    if current_user.is_anonymous or not owner_id == current_user.get_id() :
        logger.warning("Anonymous or unauthorized user "\
        "attempting notif preference update of address ID {}!".format(mid))
        return redirect(url_for('index'))

    logger.info("Entering function to update email preference..")
    mail_addr = get_email_address_by_email_id(mid)
    if mail_addr.get_notification_pref() == True:
        mail_addr.set_notification_pref(False)
    else:
        mail_addr.set_notification_pref(True)

    db.session.commit()
    return redirect(url_for('dash_email'))


@app.route('/dashboard/emails/history/<mid>')
def detection_history(mid):
    owner_id = get_owner_id_from_email_id(mid)

    if current_user.is_anonymous or not owner_id == current_user.get_id() :
        logger.warning("Anonymous or unauthorized user attempting "\
        "activation of address ID {}!".format(mid))
        return redirect(url_for('index'))

    logger.info("Entering detection history..")
    mailaddr = get_email_address_by_email_id(mid)
    mail_address = mailaddr.get_email_address()

    detection_history = db.session.query(PhishingEmail)\
    .filter(PhishingEmail.receiver_id == mid).all()
    return render_template('dashboard/detection_history.html'\
    , phishing_mails = detection_history, mail_address = mail_address)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def tos():
    return render_template('termofService.html')

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    form = ResetPasswordRequestForm()

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if form.validate_on_submit():
        user = get_user_by_name(form.username.data)
        email = get_email_address_by_address(form.email_address.data)

        if user is None:
            flash('Account does not exist!')
            return redirect(url_for('reset'))

        if user.get_active_status() == False:
            flash('Account is disabled, contact support for assistance!')
            return redirect(url_for('reset'))

        if (user and email) and user.get_id() == email.get_owner_id():
            user.generate_reset_token()
            db.session.commit()
            logger.info("Generated User Token: %s", user.get_reset_token())
            session["reset_user_id"] = user.get_id()
            send_password_token(email.get_email_address()\
            , user.get_username(), user.get_reset_token())
            return redirect(url_for('reset_change_password'))
        else:
            flash('Invalid username or email address!')
            redirect(url_for('reset'))
    return render_template('reset.html', form=form)

@app.route('/reset/change_password', methods=['GET', 'POST'])
def reset_change_password():
    form = UpdatePasswordForm()
    user = get_user_by_id(session["reset_user_id"])
    logger.info("Entering password update page")

    if form.validate_on_submit():
        token_received = form.token.data
        new_password = form.new_password.data
        logger.info("Update password form submitted")
        logger.info("User token: %s -- Token Received: %s"\
        , user.get_reset_token(), token_received)
        if user.get_reset_token() == token_received:
            logger.info("Token verified..")
            logger.info("Setting new user password and deleting reset token.")
            user.set_password(new_password)
            user.delete_reset_token()
            db.session.commit()
            flash('Password successfully changed!', 'success')
            session.pop('reset_user_id', None)
            return redirect(url_for('login'))
        else:
            flash('Invalid token!')
    return render_template('update_password.html', form=form)

@app.errorhandler(404)
def handler_404(e):
    return render_template('404.html')
