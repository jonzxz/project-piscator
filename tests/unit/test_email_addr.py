from datetime import datetime

# Test email address is set correctly
def test_email_addr_address(email_addr):
    assert email_addr.get_email_address() == 'testmail@nomail.com'

# Test email password is encrypted
def test_email_password(email_addr):
    assert not email_addr.get_email_password() == 'verySecureP@$$w0rd'

# Test decrypted email password is set correctly
def test_email_password_decrypt(email_addr):
    assert email_addr.get_decrypted_email_password() == 'verySecureP@$$w0rd'

# Test owner ID is retrieved correctly
def test_owner_id(email_addr):
    assert not email_addr.get_owner_id()

    email_addr.set_owner_id(1)
    assert email_addr.get_owner_id() == 1

# Test phishing mails detected is added correctly
def test_phishing_mail_detected(email_addr):
    assert not email_addr.get_phishing_mail_detected()
    # Initialise to 0 because of db.Integer typing returning NoneType
    email_addr.phishing_mail_detected = 0
    email_addr.set_phishing_mail_detected(10)
    assert email_addr.get_phishing_mail_detected() == 10

    email_addr.set_phishing_mail_detected(40)
    assert email_addr.get_phishing_mail_detected() == 50

# Test total mails checked is added correctly
def test_total_mails_checked(email_addr):
    assert not email_addr.get_total_mails_checked()

    # Initialise to 0 because of db.Integer typing returning NoneType
    email_addr.total_mails_checked = 0
    email_addr.set_total_mails_checked(10)
    assert email_addr.get_total_mails_checked() == 10

    email_addr.set_total_mails_checked(40)
    assert email_addr.get_total_mails_checked() == 50

# Test email address active status changes
def test_email_active_status(email_addr):
    email_addr.set_active_status(True)
    assert email_addr.get_active_status()

    email_addr.set_active_status(False)
    assert not email_addr.get_active_status()

# Test email address created at is set correctly
def test_email_created_at(email_addr):
    assert not email_addr.get_created_at()

    time = datetime.now()
    email_addr.set_created_at(time)
    assert email_addr.get_created_at() == time

# Test email address notification preference changes
def test_email_notification_pref(email_addr):
    email_addr.set_notification_pref(True)
    assert email_addr.get_notification_pref()

    email_addr.set_notification_pref(False)
    assert not email_addr.get_notification_pref()

# Test email address last updated changes
def test_email_last_updated(email_addr):
    assert not email_addr.get_last_updated()

    time = datetime.now()
    email_addr.set_last_updated(time)
    assert email_addr.get_last_updated() == time

# Test email address prettified date returns correct format and time
def test_email_pretty_date(email_addr):
    time = datetime.now()
    email_addr.set_last_updated(time)
    assert email_addr.get_prettified_date() == time.strftime('%d-%m-%Y %H:%M')
