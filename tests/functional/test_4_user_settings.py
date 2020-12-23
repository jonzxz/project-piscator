import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .test_2_authentication import login, logout
from app import db
from app.models.User import User

# Flows after deactivating email so user is in dashboard still
# Test password change in account setting by clicking into 'Account'
# and testing with valid new passwords, log out and attempt login again
def test_change_password(driver):
    USERNAME = 'testuser123'
    CUR_PASS = 'password'
    NEW_PASS = 'newpassword'
    CONF_NEW_PASS = 'newpassword'

    # Wait for navbar arrow to appear and click
    wait_nav_arrow = WebDriverWait(driver, 5)
    wait_nav_arrow.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/button')))
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/button').click()

    # Wait for account settings button to appear and click
    wait_acc_set_btn = WebDriverWait(driver, 3)
    wait_acc_set_btn.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mySidepanel"]/a[5]')))
    driver.find_element(By.XPATH, '//*[@id="mySidepanel"]/a[5]').click()
    # Assert redirected to /account page
    assert driver.current_url.split(sep='/')[-1] == 'account'

    # Wait for update button to appear (for form to appear)
    wait_update_btn = WebDriverWait(driver, 5)
    wait_update_btn.until(EC.visibility_of_element_located((By.ID, 'submit')))

    driver.find_element_by_id('current_password').send_keys(CUR_PASS)
    driver.find_element_by_id('new_password').send_keys(NEW_PASS)
    driver.find_element_by_id('confirm_new_password').send_keys(CONF_NEW_PASS)
    driver.find_element_by_id('submit').click()

    # Logs out after changing password and reattempts login with new password
    # assert log out successful
    logout(driver)
    assert driver.current_url.split(sep='/')[-1] == 'index'

    # Assert login successful with new password
    login(driver, USERNAME, NEW_PASS)
    assert driver.current_url.split(sep='/')[-1] == 'dashboard'

# Flows after password change
# Test disabling an account
def test_disable_account(driver):
    USERNAME = 'testuser123'
    PASSWORD = 'newpassword'

    # Wait for navbar arrow to appear and click
    wait_nav_arrow = WebDriverWait(driver, 5)
    wait_nav_arrow.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/button')))
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/button').click()

    # Wait for account settings button to appear
    wait_acc_set_btn = WebDriverWait(driver, 3)
    wait_acc_set_btn.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mySidepanel"]/a[5]')))
    driver.find_element(By.XPATH, '//*[@id="mySidepanel"]/a[5]').click()
    # Assert redirected to /account page
    assert driver.current_url.split(sep='/')[-1] == 'account'

    # Wait for update button to appear (for form to appear)
    wait_update_btn = WebDriverWait(driver, 5)
    wait_update_btn.until(EC.visibility_of_element_located((By.ID, 'submit')))

    # Enters current password
    # Slider for disable is actually a checkbox that must be interacted using JS
    driver.find_element_by_id('current_password').send_keys('newpassword')
    checkbox = driver.find_element_by_css_selector("#disable_acc_switch")
    driver.execute_script("arguments[0].click();", checkbox)
    driver.find_element_by_id('submit').click()

    logout(driver)
    assert driver.current_url.split(sep='/')[-1] == 'index'

    # Assert login failed so user does not go into dashboard
    login(driver, USERNAME, PASSWORD)
    assert not driver.current_url.split(sep='/')[-1] == 'dashboard'
    assert db.session.query(User).filter(User.username == USERNAME).first().get_active_status() == False