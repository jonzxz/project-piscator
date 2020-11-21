from app.models.EmailAddress import EmailAddress

def test_email_addr():
    email_addr = EmailAddress(email_address='testmail@nomail.com')
    email_addr.set_email_password('verySecureP@$$w0rd')
    email_addr.set_user_id(1)
    assert email_addr.get_email_address() == 'testmail@nomail.com'
    assert not email_addr.get_email_password() == 'verySecureP@$$w0rd'
    assert not email_addr.get_user_id() == None
