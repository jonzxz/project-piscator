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
from app.forms.ResetPasswordRequestForm import ResetPasswordRequestForm
from app.forms.UpdatePasswordForm import UpdatePasswordForm

## Models
from app.models.User import User
from app.models.EmailAddress import EmailAddress
from app.models.PhishingEmail import PhishingEmail

## Datetime
from datetime import datetime, date, timedelta
from sqlalchemy import Date, cast, func, extract

## Utils
from app.utils.EmailUtils import test_mailbox_conn
from app.utils.EmailUtils import send_contact_us_email
from app.utils.EmailUtils import get_imap_svr
from app.utils.EmailUtils import send_phish_check_notice
from app.utils.EmailUtils import send_password_token
from app.utils.DBUtils import get_user_by_id
from app.utils.DBUtils import get_user_by_name
from app.utils.DBUtils import get_email_address_by_address
from app.utils.DBUtils import get_email_address_by_email_id
from app.utils.DBUtils import get_existing_addresses_by_user_id
from app.utils.DBUtils import get_owner_id_from_email_id
from app.utils.DBUtils import check_p_mail_exist

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
    active_users = db.session.query(User).filter(User.is_active == True).count()
    detected_today = db.session.query(PhishingEmail).filter((cast(PhishingEmail.created_at, Date) == date.today())).count()
    all_time_detected = db.session.query(PhishingEmail).count()

    statistics = {
        'active_users' : active_users,
        'detected_today' : detected_today,
        'all_time_detected' : all_time_detected
    }

    contact_form = ContactForm()
    if request.method == 'POST':
        logger.debug("Email received")
        send_contact_us_email(contact_form.email_address.data, contact_form.message.data)
        return redirect(url_for('contact_form_reset'))
    return render_template('index.html', contact_form = contact_form, statistics=statistics)

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
                return redirect(url_for("reg_form_reset"))
                # return render_template('success.html', usrname = form.username.data

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
        if user.is_admin:
            return redirect(url_for('admin.index'))
        if not user.is_admin:
            return redirect(url_for('dashboard'))
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
    if current_user.is_admin:
        logger.info("Admin user logging in, redirecting to admin portal")

        # -- User statistics START
        all_users = db.session.query(User)
        users_active = all_users.filter(User.is_active==True).count()
        users_inactive = all_users.filter(User.is_active==False).count()
        logger.info("Active Users: %s -- Inactive Users: %s", users_active, users_inactive)
        user_stats = [users_inactive, users_active]
        # -- User statistics END

        # -- Email statistics START
        all_emails = db.session.query(EmailAddress)
        email_active = all_emails.filter(EmailAddress.active==True).count()
        email_inactive = all_emails.filter(EmailAddress.active==False).count()
        logger.info("Active Email Address: %s -- Inactive Email Address: %s" \
        , email_active, email_inactive)
        email_stats = [email_inactive, email_active]
        # -- Email statistics END

        # -- Phishing Emails Overview START
        all_time_detected = db.session.query(PhishingEmail) \
        .filter(PhishingEmail.receiver_id==EmailAddress.email_id)

        today_detected = all_time_detected \
        .filter((cast(PhishingEmail.created_at, Date) == date.today()))

        weekly_detected = all_time_detected \
        .filter(PhishingEmail.created_at_week == datetime.now().isocalendar()[1])

        # Likewise for month, same as week
        monthly_detected = all_time_detected \
        .filter(PhishingEmail.created_at_month == datetime.now().month \
        , PhishingEmail.created_at_year == datetime.now().year)

        statistics = {
            'user_stats' : [users_active, users_inactive],
            'email_stats' : [email_active, email_inactive],
            'all_time' : all_time_detected.count(),
            'monthly' : monthly_detected.count(),
            'weekly' : weekly_detected.count(),
            'today' : today_detected.count()
        }

        monthly_stats = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
            10: 0,
            11: 0,
            12: 0
        }

        month = func.date_trunc('month', func.cast(PhishingEmail.created_at, Date))

        # Returns a list of PE owned by cur_user's all email addresses that was detected
        # in the current year
        mails_detected_yearly = db.session.query(PhishingEmail) \
        .filter(PhishingEmail.receiver_id==EmailAddress.email_id \
        , PhishingEmail.created_at_year == datetime.now().year) \
        .order_by(month).all() # Order_by not needed but might be faster for dict traversals??

        for pe in mails_detected_yearly:
            monthly_stats[pe.get_created_month()] = monthly_stats.get(pe.get_created_month(), 0)+1
        monthly_stats = list(monthly_stats.values())
        # -- Phishing Emails Overview END
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
    if current_user.is_admin:
        logger.info("Admin logging in, redirecting to admin portal")
        return redirect(url_for('admin.index'))
    logger.info("User logging in, redirecting to users portal")

    # -- Email Address Status Count START
    all_emails = db.session.query(EmailAddress).filter(EmailAddress.owner_id==current_user.user_id)
    email_active = all_emails.filter(EmailAddress.active==True).count()
    email_inactive = all_emails.filter(EmailAddress.active==False).count()
    logger.info("Active Email Address: %s -- Inactive Email Address: %s" \
    , email_active, email_inactive)
    email_stats = all_emails.count()
    # -- Email Address Status count END

    # -- Phishing Emails Overview START
    all_time_detected = db.session.query(PhishingEmail) \
    .filter(PhishingEmail.receiver_id==EmailAddress.email_id \
    , EmailAddress.owner_id==current_user.user_id)

    today_detected = all_time_detected \
    .filter((cast(PhishingEmail.created_at, Date) == date.today()))

    weekly_detected = all_time_detected \
    .filter(PhishingEmail.created_at_week == datetime.now().isocalendar()[1])

    # Likewise for month, same as week
    monthly_detected = all_time_detected \
    .filter(PhishingEmail.created_at_month == datetime.now().month \
    , PhishingEmail.created_at_year == datetime.now().year)

    logger.info("All Time Detection: %s -- Today Detection: %s \
    -- Weekly Detection: %s -- Monthly Detection: %s" \
    , all_time_detected.count(), today_detected.count() \
    , weekly_detected.count(), monthly_detected.count())

    statistics = {
        'all_time' : all_time_detected.count(),
        'today' : today_detected.count(),
        'weekly' : weekly_detected.count(),
        'monthly' : monthly_detected.count(),
        'email_active' : email_active,
        'email_inactive' : email_inactive,
        'email_stats' : email_stats,
    }

    monthly_stats = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0
    }

    month = func.date_trunc('month', func.cast(PhishingEmail.created_at, Date))

    # Returns a list of PE owned by cur_user's all email addresses that was detected
    # in the current year
    mails_detected_yearly = db.session.query(PhishingEmail) \
    .filter(PhishingEmail.receiver_id==EmailAddress.email_id \
    , EmailAddress.owner_id==current_user.user_id \
    , PhishingEmail.created_at_year == datetime.now().year) \
    .order_by(month).all() # Order_by not needed but might be faster for dict traversals??

    for pe in mails_detected_yearly:
        monthly_stats[pe.get_created_month()] = monthly_stats.get(pe.get_created_month(), 0)+1
    monthly_stats = list(monthly_stats.values())
    # -- Phishing Emails Overview END

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
    change_email_password_form = change_email_password_form, user_emails = existing_addresses)
    ## -- Default Dashboard Loading END --

@app.route('/dashboard/add_email', methods=['POST'])
def add_email():
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
            # -- If you want to test adding emails to a user account without checking connection
            # -- change the if statement to if True:
            # if test_mailbox_conn(email_addr, password):
            if True:
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
                flash("Unable to connect to mailbox.")
        else:
            flash("{} already exist in our database!".format(email_addr))
            logger.error("Email already exist")
            return redirect(url_for('mail_form_reset'))
    ## -- Add Email Form submission END --

    return redirect(url_for('dash_email'))

@app.route('/dashboard/update_email_password', methods=['POST'])
def update_email_password():
    logger.info("ENTERED START FUNC: UPDATE_EMAIL_PASS")
    add_email_form = AddEmailForm()
    change_email_password_form = ChangeEmailPasswordForm()
    existing_addresses = get_existing_addresses_by_user_id(current_user.user_id)

    if change_email_password_form.is_submitted():
        logger.info("Change email password form submitted.")
        logger.info("EMAIL ADDR RECEIVED: %s", change_email_password_form.email_address.data)
        email_addr = change_email_password_form.email_address.data
        email_address = get_email_address_by_address(email_addr)

        logger.info("Entering password change")
        if email_address is not None and email_address.get_active_status():
            if change_email_password_form.new_password.data:
                if test_mailbox_conn(email_addr, change_email_password_form.new_password.data):
                    flash('Password successfully updated!', 'success')
                    email_address.set_email_password(change_email_password_form.new_password.data)
                    db.session.commit()
                else:
                    flash('Unable to connect to mailbox with new password!', 'error')
            else:
                logger.info("Password entered is empty.")
                flash('Password entered for update password is empty.', 'error')
                return redirect(url_for('mail_form_reset'))
        else:
                logger.info("Email address is inactive or None.")
                flash('Email address is inactive or does not exist', 'error')
                return redirect(url_for('mail_form_reset'))
                # -- Change the Email Password END --

    return redirect(url_for('dash_email'))

@app.route('/dashboard/account', methods=['GET', 'POST'])
def dash_account():
    logger.info("Entering dashboard account..")
    if current_user.is_anonymous:
        logger.warning("Anonymous user in dashboard account, going to index..")
        return redirect(url_for('index'))

    form = AccountSettingsForm()
    #logger.info(current_user.username)
    #logger.info(form.current_password.data)
    user = get_user_by_id(current_user.user_id)
    status = user.get_active_status()

    if form.validate_on_submit():
        logger.info("%s submitted account settings form", user.get_username())

        # If not password is entered, error is caught on Form level

        # Current password required for changing password / disabling of account
        # both change in state and change of password requires the correct current password
        if not user.check_password(form.current_password.data):
            logger.info("%s submitted wrong password, redirecting to dashboard", user.get_username())
            flash('Invalid Current Password!')
            return redirect(url_for('dash_account'))

        # Retrieve slider data
        disable_account = request.form.get('disable_account')

        logger.info("%s -- Active: %s -- DisableSlider: %s",
        user.get_username(), user.get_active_status(), disable_account)

        # note: if all fields (current, new, confirm new passwords and disabled account) are filled
        # only disable / enable account will be triggered, password will not be updated

        ## -- Password Change START --
        #check for state change (db vs form)
        #if user is active and form state is None (both means account is active) -> no change
        #or user is inactive and form state is True (both means account is inactive) -> no change
        if (user.get_active_status() and disable_account is None) or (not user.get_active_status() and disable_account == "on"): # line does nothing for now, if user is disabled they cannot log in
            # since no change in state, check for password change then
            logger.info("Entering password change")
            status = user.get_active_status()
            if user is not None and user.check_password(form.current_password.data):
                if not form.new_password.data or not form.confirm_new_password.data:
                    logger.info("Either password fields are empty, redirecting.")
                    flash('Please enter a new password to change passwords or select disable account to disable your account.')
                    return redirect(url_for('dash_account'))
                elif form.new_password.data == form.confirm_new_password.data:
                    logger.info("Password changed for %s", user.get_username())
                    user.set_password(form.new_password.data)
                    flash('Password Successfully Changed!')
                else:
                    logger.info("Mismatched passwords submited, redirecting.")
                    flash('Passwords does not match!')
                    return redirect(url_for('dash_account'))
            else:
                logger.info("Invalid current password submitted, redirecting.")
                flash('Invalid \'Current Password\'!')
                return redirect(url_for('dash_account'))
        ## -- Password Change END --
        ## -- Account State START --
        else:
            logger.info("Entering account enable/disable.")
            # Change in state, disable/enable account
            if user is not None and user.check_password(form.current_password.data):
                if disable_account == "on":
                    #to change is_active state to False -> disable account
                    #to disable account
                    user.set_active_status(False)
                    logger.info("Setting %s account status to disabled", user.get_username())
                    logger.info("Sleeping for 3 seconds before logging out user")
                    # Sets all email addresses for user to disabled
                    user_emails = get_existing_addresses_by_user_id(user.user_id)
                    for email in user_emails:
                        logger.info("Disabling %s", email)
                        email.set_active_status(False)

                    flash('Account is Disabled!')
                # This block does nothing for now, disabled users cannot log in
                elif disable_account is None:
                    #to change is_active state to True -> enable account
                    #to disable account
                    user.set_active_status(True)
                    logger.info("Setting %s account status to enabled", user.get_username())

                    flash('Account is Enabled!')
            else:
                flash('Invalid \'Current Password\'!')
                logger.info("User %s entered invalid current password", user.get_username())
                return redirect(url_for('dash_account'))
            # Password change requested together with account activation, latter take precedence
            # No changes in password will execute.
            if form.new_password.data or form.confirm_new_password.data:
                logger.info("Activation and password triggered - password not updated.")
                flash('Password is not changed!')
        ## -- Account State END --

        try:
            db.session.commit()
            logger.debug("Successfully changed user %s password, updated database", user)
            return redirect(url_for('dash_account'))
        except IntegrityError:
            db.session.rollback()
            logger.error("Failed to change password for %s, rolling back database", user)

    # Updates values of status after changing status, does not do anything right now
    # as user cannot log in after disabling account.
    status = user.get_active_status()
    return render_template('dashboard/dashboard_account.html',
    current_user = current_user.username, form = form, status = status)


@app.route('/dashboard/emails/phish/<mid>')
def check_phish(mid):
    phishing_mails = []

    # Retrieves the email address instance
    logger.info("Click-to-check entered..")

    owner_id = get_owner_id_from_email_id(mid)
    if current_user.is_anonymous or not owner_id == current_user.get_id() :
        logger.warning("Anonymous or unauthorized user attempting phish check of address ID {}!".format(mid))
        return redirect(url_for('index'))

    mailaddr = get_email_address_by_email_id(mid)

    # Redirects back to page if selected email is inactive
    if mailaddr.get_active_status() == False:
        logger.warning("Redirecting.. User selected inactive email address %s", mailaddr.get_email_address())
        flash("Email is inactive!")
        return redirect(url_for('dash_email'))

    logger.info("Mailbox selected is %s", mailaddr.get_email_address())

    try:
        # Logs in to mailbox by retrieving the corresponding IMAP server
        imap_svr = get_imap_svr(mailaddr.get_email_address())
        logger.info("Retrieving IMAP server: %s", imap_svr)
        mailbox = MailBox(imap_svr)
        logger.info("Attempting connection..")
        mailbox.login(mailaddr.get_email_address(), mailaddr.get_decrypted_email_password())
        logger.info("Connected to mailbox %s", mailaddr.get_email_address())
    except ConnectionRefusedError:
        logger.error("Unable to connect to mailbox for %s", mailaddr.get_email_address())
        flash("Unable to connect to mailbox!")
        return redirect(url_for('dash_email'))

    # Retrieves date last updated: converts datetime to date
    last_updated = mailaddr.get_last_updated().date() if mailaddr.get_last_updated() else datetime.now().date()
    # Updates last updated to current time
    mailaddr.set_last_updated(datetime.now())
    logger.info("Updating mailbox last updated from %s to %s",\
     last_updated.strftime("%d-%m-%Y"), datetime.now())

    # Selects mailbox to Inbox only
    mailbox.folder.set("INBOX")
    logger.info("Fetching mails..")

    # Sets a check criteria so that
    # only mails newer than last_updated and unread mails are checked
    # check_criteria = AND(date_gte=last_updated, seen=False)

    check_criteria = AND(date_gte=[date(2020, 12, 17)], seen=False)

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

    for msg in all_mails:
        try:
            sender = msg.from_
        except HeaderParseError:
            # Exception happens when a msg.from_ is malformed resulting in
            # unparseable values. Automatically assume phishing email and add to record.
            # Denote Sender as 'INVALID_SENDER'
            logger.error("HeaderParseError, unparseable msg.from_. Setting sender as INVALID_SENDER")
            sender = 'INVALID_SENDER'

        if not sender == mailaddr.get_email_address() or not sender == 'piscator.fisherman@gmail.com':
            # logger.info("Checking mail subject: %s -- date sent: %s", msg.subject, (msg.date).strftime("%d-%m-%Y"))
            data['total_count']+=1
            mail_item = EmailData(msg.subject, sender, msg.attachments, (msg.text + msg.html), msg.headers)
            mail_item.generate_features()
            result = model.predict(mail_item.repr_in_arr())
            logger.info("Checking mail: %s -- Result: %s", mail_item.get_subject(), result)
            if result == 1:
                logger.info("Phishing mail detected, subject: %s", msg.subject)

                mail_exist = check_p_mail_exist(mailaddr.get_email_id()\
                , msg.subject, mail_item.get_content())

                if not mail_exist:
                    phishing_mails.append(Mail(sender, msg.date, msg.subject))
                    data['detection_count']+=1
                    detected_mail = PhishingEmail( \
                    sender_address = sender, \
                    subject = msg.subject, \
                    content = mail_item.get_content(), \
                    created_at = datetime.now(), \
                    receiver_id = mailaddr.get_email_id()
                    )
                    db.session.add(detected_mail)

    mailaddr.set_phishing_mail_detected(data['detection_count'])
    db.session.commit()
    logger.info("Finished checking mails.. logging out")
    mailbox.logout()
    send_phish_check_notice(mailaddr.get_email_address(), phishing_mails)

    mailaddr = get_email_address_by_email_id(mid)
    mail_address = mailaddr.get_email_address()
    logger.info(mailaddr)
    logger.info(mail_address)

    # return redirect(url_for('dashboard'))
    return render_template('dashboard/detection_results.html', \
    phishing_mails = phishing_mails, data=data, mail_address = mail_address)

@app.route('/dashboard/emails/activation/<mid>')
def mail_activation(mid):
    owner_id = get_owner_id_from_email_id(mid)

    if current_user.is_anonymous or not owner_id == current_user.get_id() : # or CU ID is not owner of MID
        logger.warning("Anonymous or unauthorized user attempting activation of address ID {}!".format(mid))
        return redirect(url_for('index'))

    logger.info("Entering function to enable/disable email..")
    mailaddr = get_email_address_by_email_id(mid)
    if mailaddr.get_active_status() == True:
        mailaddr.set_active_status(False)
    else:
        mailaddr.set_active_status(True)
    db.session.commit()
    return redirect(url_for('dash_email'))

@app.route('/dashboard/emails/history/<mid>')
def detection_history(mid):
    owner_id = get_owner_id_from_email_id(mid)

    if current_user.is_anonymous or not owner_id == current_user.get_id() : # or CU ID is not owner of MID
        logger.warning("Anonymous or unauthorized user attempting activation of address ID {}!".format(mid))
        return redirect(url_for('index'))

    mailaddr = get_email_address_by_email_id(mid)
    mail_address = mailaddr.get_email_address()

    detection_history = db.session.query(PhishingEmail).filter(PhishingEmail.receiver_id == mid).all()
    logger.info(detection_history)
    logger.info(mailaddr)
    logger.info(mail_address)
    return render_template('dashboard/detection_history.html', phishing_mails = detection_history \
    , mail_address = mail_address)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def tos():
    return render_template('termofService.html')

# Reroute functions to prevent form resubmission on refresh
@app.route('/mail_form_reset', methods=['GET'])
def mail_form_reset():
    logger.info("Entering function to reset form submission")
    return redirect(url_for('dash_email'))

@app.route('/reg_form_reset', methods=['GET'])
def reg_form_reset():
    logger.info("Entering function to reset form submission")
    return redirect(url_for('register'))

@app.route('/contact_form_reset', methods=['GET'])
def contact_form_reset():
    return redirect(url_for('index'))

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
            send_password_token(email.get_email_address(), user.get_username(), user.get_reset_token())
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
        logger.info("User token: %s -- Token Received: %s", user.get_reset_token(), token_received)
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
