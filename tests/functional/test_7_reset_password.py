import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .test_2_authentication import login, logout
from app.models.User import User
from app import db
from time import sleep

# Flows from test_6 admin edit user, starts from index
def test_request_reset_password(driver):
    # Uses back the same user created and tested in tests 2, 3, 4
    USERNAME = 'testuser123'
    EMAIL_ADDR = 'testmail456@mymail.com'

    # enables back the user from DB first
    user = db.session.query(User).filter(User.username == USERNAME).first()
    user.update_active_status(True)
    db.session.commit()

    # Assert user successfully enabled via database access
    assert (db.session.query(User).filter(User.username == USERNAME).first()).get_active_status() == True

    # Click 'Sign In' from index
    wait_login_btn = WebDriverWait(driver, 5)
    wait_login_btn.until(EC.visibility_of_element_located((By.XPATH, '/html/body/header/div[1]/div/div/div/nav/div[2]/a')))
    driver.find_element(By.XPATH, '/html/body/header/div[1]/div/div/div/nav/div[2]/a').click()

    # Click forget your password? button
    wait_forget_btn = WebDriverWait(driver, 5)
    wait_forget_btn.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/div[5]/div/div/a')))
    driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/div[5]/div/div/a').click()

    # Assert redirected to reset page
    assert driver.current_url.split(sep='/')[-1] == 'reset'

    wait_reset_btn = WebDriverWait(driver, 5)
    wait_reset_btn.until(EC.visibility_of_element_located((By.ID, 'submit')))
    driver.find_element_by_id('username').send_keys(USERNAME)
    driver.find_element_by_id('email_address').send_keys(EMAIL_ADDR)
    driver.find_element_by_id('submit').click()

    # Assert redirected to reset page
    assert driver.current_url.split(sep='/')[-1] == 'change_password'

def test_update_password(driver):
    USERNAME = 'testuser123'
    TEST_RESET_PASSWORD = 'iforgotmypassword'

    USER_UPDATED = db.session.query(User).filter(User.username == USERNAME).first()

    # Assert token is generated
    assert USER_UPDATED.get_reset_token()

    # Retrieves token value from db and submits into the field with new password
    USER_TOKEN = str(USER_UPDATED.get_reset_token())
    wait_submit_reset_btn = WebDriverWait(driver, 5)
    wait_submit_reset_btn.until(EC.visibility_of_element_located((By.ID, 'submit')))
    driver.find_element_by_id('token').send_keys(USER_TOKEN)
    driver.find_element_by_id('new_password').send_keys(TEST_RESET_PASSWORD)
    driver.find_element_by_id('submit').click()

    # Assert redirected to login
    assert driver.current_url.split(sep='/')[-1] == 'login'

    # Enter credentials
    driver.find_element_by_id('username').send_keys(USERNAME)
    driver.find_element_by_id('password').send_keys(TEST_RESET_PASSWORD)
    driver.find_element_by_id('submit').click()

    assert driver.current_url.split(sep='/')[-1] == 'dashboard'
