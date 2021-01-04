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
    href_link = '//a[@href="{}"]'.format('/admin/user/edit/?id={}&url=%2Fadmin%2Fuser%2F&modal=True'.format(user_to_disable_id))
    wait_user_entry = WebDriverWait(driver, 5)
    wait_user_entry.until(EC.visibility_of_element_located((By.XPATH, href_link)))
    driver.find_element(By.XPATH, href_link).click()

    # The sleep(2) is required otherwise wait_active_box does not work
    sleep(2)
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
    wait_submit.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="fa_modal_window"]/div/div/form/fieldset/div[2]/input')))
    driver.find_element(By.XPATH, '//*[@id="fa_modal_window"]/div/div/form/fieldset/div[2]/input').send_keys(Keys.RETURN)

    # Finally redirects to list view again after editing user status
    # The database is actually updated at this point
    # But Assertion statement fails here for some reason - 20/12/20 Jon K
    # ***Check for this test is done in the next test***

# As mentioned above, assertion have to be done in a separate test
# in order to reflect the correct user active status, no idea why - 25/12/20 Jon K
def test_assert_disable_user(driver):
    TEST_DISABLE_USER = 'disableme'
    updated_user = db.session.query(User).filter(User.username == TEST_DISABLE_USER).first()
    assert updated_user.get_active_status() == False


def test_enable_user(driver):
    TEST_ENABLE_USER = 'disableme'

    # Search for newly created user for it's ID
    user_to_enable = db.session.query(User).filter(User.username ==TEST_ENABLE_USER).first()
    user_to_enable_id = user_to_enable.get_id()

    # Clicks on 'Users' in admin navbar
    wait_user_btn = WebDriverWait(driver, 3)
    wait_user_btn.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mySidepanel"]/a[2]')))
    driver.find_element(By.XPATH, '//*[@id="mySidepanel"]/a[2]').click()

    # Searches for edit (a pencil in 1st column) by href where it's url is href_link
    # and click to enter edit page for the particular user
    href_link = '//a[@href="{}"]'.format('/admin/user/edit/?id={}&url=%2Fadmin%2Fuser%2F&modal=True'.format(user_to_enable_id))
    wait_user_entry = WebDriverWait(driver, 5)
    wait_user_entry.until(EC.visibility_of_element_located((By.XPATH, href_link)))
    driver.find_element(By.XPATH, href_link).click()

    # The sleep(2) is required otherwise wait_active_box does not work
    sleep(2)
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
    wait_submit.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="fa_modal_window"]/div/div/form/fieldset/div[2]/input')))
    driver.find_element(By.XPATH, '//*[@id="fa_modal_window"]/div/div/form/fieldset/div[2]/input').send_keys(Keys.RETURN)

    # Finally redirects to list view again after editing user status
    # The database is actually updated at this point
    # But Assertion statement fails here for some reason - 20/12/20 Jon K
    # ***Check for this test is done in the next test***

# As mentioned above, assertion have to be done in a separate test
# in order to reflect the correct user active status, no idea why - 25/12/20 Jon K
def test_assert_enable_user(driver):
    TEST_ENABLE_USER = 'disableme'
    updated_user = db.session.query(User).filter(User.username == TEST_ENABLE_USER).first()
    assert updated_user.get_active_status() == True

    # Logout back to index
    wait_logout = WebDriverWait(driver, 5)
    wait_logout.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mySidepanel"]/a[5]')))
    driver.find_element(By.XPATH, '//*[@id="mySidepanel"]/a[5]').click()

    # Assert redirected to index
    assert driver.current_url.split(sep='/')[-1] == 'index'
