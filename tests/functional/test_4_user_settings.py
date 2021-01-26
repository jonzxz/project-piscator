import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .test_2_authentication import login, logout
from app import db
from time import sleep
from app.models.User import User

# Flows after deactivating email so user is in dashboard still
# Test password change in account setting by clicking into 'Account'
#To submit form with no input
def test_change_password_no_input(driver):
    USERNAME = 'testuser123'
    MISSING_PASSWORD_ERR = 'Invalid Current Password!'

    # Wait for account settings button to appear and click
    wait_acc_set_btn = WebDriverWait(driver, 3)
    wait_acc_set_btn.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="user-panel"]/a[4]')))
    driver.find_element(By.XPATH, '//*[@id="user-panel"]/a[4]').click()
    # Assert redirected to /account page
    assert driver.current_url.split(sep='/')[-1] == 'account'

    # Wait for update button to appear (for form to appear)
    wait_update_btn = WebDriverWait(driver, 5)
    wait_update_btn.until(EC.visibility_of_element_located((By.ID, 'update_password_submit')))
    assert USERNAME in driver.page_source

    driver.find_element_by_id('update_password_submit').click()

    assert MISSING_PASSWORD_ERR in driver.page_source

#To submit form with invalid current password
def test_change_invalid_current_password(driver):
    USERNAME = 'testuser123'
    CUR_PASS = 'password123'
    NEW_PASS = 'newpassword'
    CONF_NEW_PASS = 'newpassword'
    CURRENT_PASSWORD_ERR = 'Invalid Current Password!'

    assert USERNAME in driver.page_source

    driver.find_element_by_id('current_password').send_keys(CUR_PASS)
    driver.find_element_by_id('new_password').send_keys(NEW_PASS)
    driver.find_element_by_id('confirm_new_password').send_keys(CONF_NEW_PASS)
    driver.find_element_by_id('update_password_submit').click()

    assert CURRENT_PASSWORD_ERR in driver.page_source

#To submit form with different new password and confirm new password
def test_change_different_new_password(driver):
    USERNAME = 'testuser123'
    CUR_PASS = 'password'
    NEW_PASS = 'newpassword'
    CONF_NEW_PASS = 'newpassword123'
    DIFFERENT_PASSWORD_ERR = 'New Password and Confirm New Password must match!'

    assert USERNAME in driver.page_source

    driver.find_element_by_id('current_password').send_keys(CUR_PASS)
    driver.find_element_by_id('new_password').send_keys(NEW_PASS)
    driver.find_element_by_id('confirm_new_password').send_keys(CONF_NEW_PASS)
    driver.find_element_by_id('update_password_submit').click()

    assert DIFFERENT_PASSWORD_ERR in driver.page_source

# and testing with valid new passwords, log out and attempt login again
def test_change_password(driver):
    USERNAME = 'testuser123'
    CUR_PASS = 'password'
    NEW_PASS = 'newpassword'
    CONF_NEW_PASS = 'newpassword'
    CHANGE_PASSWORD_SUCCESS = 'Password Successfully Changed!'

    driver.find_element_by_id('current_password').send_keys(CUR_PASS)
    driver.find_element_by_id('new_password').send_keys(NEW_PASS)
    driver.find_element_by_id('confirm_new_password').send_keys(CONF_NEW_PASS)
    driver.find_element_by_id('update_password_submit').click()

    assert CHANGE_PASSWORD_SUCCESS in driver.page_source

    # Logs out after changing password and reattempts login with new password
    # assert log out successful
    logout(driver)
    assert driver.current_url.split(sep='/')[-1] == 'index'

    # Assert login successful with new password
    login(driver, USERNAME, NEW_PASS)
    assert driver.current_url.split(sep='/')[-1] == 'dashboard'

def disable_acc_navtab(driver):
    # Wait for account settings button to appear
    wait_acc_set_btn = WebDriverWait(driver, 3)
    wait_acc_set_btn.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="user-panel"]/a[4]')))
    driver.find_element(By.XPATH, '//*[@id="user-panel"]/a[4]').click()
    # Assert redirected to /account page
    assert driver.current_url.split(sep='/')[-1] == 'account'

    # Wait for "Disable Account" navtab to appear
    wait_nav_disable_acc_tab = WebDriverWait(driver, 3)
    wait_nav_disable_acc_tab.until(EC.visibility_of_element_located((By.ID, 'nav-disable-account')))
    driver.find_element(By.ID, 'nav-disable-account').click()

    wait_disable_submit = WebDriverWait(driver, 3)
    wait_disable_submit.until(EC.visibility_of_element_located((By.ID, 'disable_acc_submit')))

# Flows after password change
#To submit form with correct password but without selecting the disable account slider_data
def test_without_slider_disable_account(driver):
    USERNAME = 'testuser123'
    PASSWORD = 'newpassword'
    INVALID_DISABLE_ACC_ERR = 'If you intend to disable your account, click the slider!'

    disable_acc_navtab(driver)

    driver.find_element_by_id('disable_acc_current_password').send_keys(PASSWORD)
    driver.find_element_by_id('disable_acc_submit').click()

    assert driver.current_url.split(sep='/')[-1] == 'account'
    assert INVALID_DISABLE_ACC_ERR in driver.page_source

#To submit form without password but selected the slider
def test_without_password_disable_account(driver):
    USERNAME = 'testuser123'
    INVALID_DISABLE_ACC_PASS_ERR = 'Invalid Current Password!'

    disable_acc_navtab(driver)

    checkbox = driver.find_element_by_css_selector("#disable_acc_switch")
    driver.execute_script("arguments[0].click();", checkbox)
    sleep(3)
    driver.find_element_by_id('disable_acc_submit').click()

    assert driver.current_url.split(sep='/')[-1] == 'account'
    assert INVALID_DISABLE_ACC_PASS_ERR in driver.page_source

#To submit form with invalid password and with slider
def test_wrong_password_disable_account(driver):
    USERNAME = 'testuser123'
    PASSWORD = 'newpassword1'
    INVALID_DISABLE_ACC_PASS_ERR = 'Invalid Current Password!'

    disable_acc_navtab(driver)

    driver.find_element_by_id('disable_acc_current_password').send_keys(PASSWORD)
    checkbox = driver.find_element_by_css_selector("#disable_acc_switch")
    driver.execute_script("arguments[0].click();", checkbox)
    sleep(3)
    driver.find_element_by_id('disable_acc_submit').click()

    assert driver.current_url.split(sep='/')[-1] == 'account'
    assert INVALID_DISABLE_ACC_PASS_ERR in driver.page_source

# Test disabling an account
def test_disable_account(driver):
    USERNAME = 'testuser123'
    PASSWORD = 'newpassword'
    DISABLE_LOGOUT_MSG = 'Account is Disabled! You\'ll be logged out in 5 seconds..'
    ACCOUNT_IS_DISABLED = 'Account is disabled, contact support!'

    disable_acc_navtab(driver)

    # Enters current password
    # Slider for disable is actually a checkbox that must be interacted using JS
    driver.find_element_by_id('disable_acc_current_password').send_keys(PASSWORD)
    checkbox = driver.find_element_by_css_selector("#disable_acc_switch")
    driver.execute_script("arguments[0].click();", checkbox)
    sleep(3)
    driver.find_element_by_id('disable_acc_submit').click()

    assert DISABLE_LOGOUT_MSG in driver.page_source
    wait_home = WebDriverWait(driver, 10)
    wait_home.until(EC.visibility_of_element_located((By.ID, 'home-nav')))
    assert driver.current_url.split(sep='/')[-1] == 'index'

    # Assert login failed so user does not go into dashboard
    login(driver, USERNAME, PASSWORD)
    assert driver.current_url.split(sep='/')[-1] != 'dashboard'
    assert db.session.query(User).filter(User.username == USERNAME).first().get_active_status() == False
    assert ACCOUNT_IS_DISABLED in driver.page_source
