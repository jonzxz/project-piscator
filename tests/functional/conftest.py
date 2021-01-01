import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import os

from app import db
from app.models.EmailAddress import EmailAddress

@pytest.fixture(scope='session')
def driver():
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get('localhost:5000')
    yield driver
    driver.quit()


""" Run after all tests
    mail = db.session.query(EmailAddress).filter(EmailAddress.email_address == 'testmail456@mymail.com').first()
    db.session.delete(mail)
    user = db.session.query(User).filter(User.username == 'testuser123')
    db.session.delete(user)
    db.session.commit()
"""
