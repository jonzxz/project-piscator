import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .test_2_authentication import login, logout
from app.models.User import User
from app import db
from time import sleep

# Flows from test_5 admin logout so this starts from homepage
# Creates a new dummy user via direct DB access to be tested on
# Logs in using utility login function, retrieves new user ID, disable active status of user.
def test_admin_disable_user(driver):

    TEST_DISABLE_USER = 'disableme'
    TEST_DISABLE_PASSWORD = 'password'

    # Creation of dummy user
    new_user = User(username=TEST_DISABLE_USER)
    new_user.set_password(TEST_DISABLE_PASSWORD)
    db.session.add(new_user)
    db.session.commit()

    # Logs in to admin dashboard
    ADMIN_USER = 'admin'
    PASSWORD = 'password'
    login(driver, ADMIN_USER, PASSWORD)

    # Search for newly created user for it's ID
    user_to_disable = db.session.query(User).filter(User.username ==TEST_DISABLE_USER).first()
    user_to_disable_id = user_to_disable.get_id()

    # Clicks on 'Users' in admin navbar
    wait_user_btn = WebDriverWait(driver, 3)
    wait_user_btn.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mySidepanel"]/a[2]')))
    driver.find_element(By.XPATH, '//*[@id="mySidepanel"]/a[2]').click()

    # Searches for edit (a pencil in 1st column) by href where it's url is href_link
    # and click to enter edit page for the particular user
    href_link = '//a[@href="{}"]'.format('/admin/user/edit/?id={}&url=%2Fadmin%2Fuser%2F'.format(user_to_disable_id))
    wait_user_entry = WebDriverWait(driver, 5)
    wait_user_entry.until(EC.visibility_of_element_located((By.XPATH, href_link)))
    driver.find_element(By.XPATH, href_link).click()

    # Unchecks active checkbox
    wait_active_box = WebDriverWait(driver, 3)
    wait_active_box.until(EC.visibility_of_element_located((By.ID, 'is_active')))
    checkbox = driver.find_element_by_css_selector("#is_active")
    driver.execute_script("arguments[0].click();", checkbox)

    # Clicks "Save" in edit page
    # The click here is done by send_keys(Keys.RETURN) simulating enter on the key
    # And the sleep(2) is required otherwise the click will NOT work sometimes
    sleep(2)
    wait_submit = WebDriverWait(driver, 3)
    wait_submit.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/form/fieldset/div[7]/div/input[1]')))
    driver.find_element(By.XPATH, '/html/body/div[1]/form/fieldset/div[7]/div/input[1]').send_keys(Keys.RETURN)

    # Finally redirects to list view again after editing user status
    # The database is actually updated at this point
    # But Assertion statement fails here for some reason - 20/12/20 Jon K
    # ***Check for this test is done in the next test***

def test_admin_change_user(driver):
    TEST_DISABLE_USER = 'disableme'
    TEST_DISABLE_PASSWORD = 'password'
    NEW_USERNAME = 'iamdisabled'

    # Search for dummy user for it's ID
    user_id = db.session.query(User).filter(User.username == TEST_DISABLE_USER).first().get_id()

    # Searches for edit (a pencil in 1st column) by href where it's url is href_link
    # and click to enter edit page for the particular user
    href_link = '//a[@href="{}"]'.format('/admin/user/edit/?id={}&url=%2Fadmin%2Fuser%2F'.format(user_id))
    wait_user_entry = WebDriverWait(driver, 3)
    wait_user_entry.until(EC.visibility_of_element_located((By.XPATH, href_link)))
    driver.find_element(By.XPATH, href_link).click()

    # Waits for the edit page (in particular the username field) to load
    # Clears the fields and enters a new username
    wait_user_field = WebDriverWait(driver, 3)
    wait_user_field.until(EC.visibility_of_element_located((By.ID, 'username')))
    driver.find_element(By.ID, 'username').clear()
    driver.find_element(By.ID, 'username').send_keys(NEW_USERNAME)

    # Clicks "Save" in edit page
    # The click here is done by send_keys(Keys.RETURN) simulating enter on the key
    # And the sleep(2) is required otherwise the click will NOT work sometimes
    sleep(2)
    wait_submit = WebDriverWait(driver, 3)
    wait_submit.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/form/fieldset/div[7]/div/input[1]')))
    driver.find_element(By.XPATH, '/html/body/div[1]/form/fieldset/div[7]/div/input[1]').send_keys(Keys.RETURN)

    # Retrieves a new entity for user after updating username
    # Performs assertion for the previous test and this test
    # not active and current username is not the previous username
    updated_user = db.session.query(User).filter(User.user_id == user_id).first()
    assert updated_user.get_active_status() == False
    assert not updated_user.get_username() == TEST_DISABLE_USER
