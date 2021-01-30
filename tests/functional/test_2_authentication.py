import pytest
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Reusable function to provide login automation from homepage
# Clicks sign in and enters credentials as provided
def login(driver, username, password):
    # Click 'Sign In'
    wait_login_btn = WebDriverWait(driver, 5)
    wait_login_btn.until(EC.element_to_be_clickable((By.XPATH\
    , '//*[@id="navbar"]/div[2]/a')))
    driver.find_element(By.XPATH, '//*[@id="navbar"]/div[2]/a').click()
    # Enter credentials
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('submit').click()

# Reusable function to provide USER logout automation from dashboard
# clicks the nav bar arrow and clicks sign out
def logout(driver):
    # Waits for logout button to appear and click
    wait_logout = WebDriverWait(driver, 5)
    wait_logout.until(EC.visibility_of_element_located((By.XPATH\
    , '//*[@id="user-panel"]/a[5]')))
    driver.find_element(By.XPATH, '//*[@id="user-panel"]/a[5]').click()

# Test registering a user from homepage
# Clicks on 'Get Started', enter register credentials and check user is redirected to dashboard
# Finally logs out

# Test invalid register with empty fields
def test_register_no_input(driver):
    REQUIRED_FIELD_ERR = 'This field is required.'
    TOS_POLICIES_ERR = 'You must agree to the terms and policies to register!'

    # Click 'Get Started'
    driver.find_element(By.XPATH, '//*[@id="home"]/div[1]/div[1]/div/div/a').click()
    assert driver.current_url.split(sep='/')[-1] == 'register'

    driver.find_element_by_id('submit').click()
    assert driver.current_url.split(sep='/')[-1] != 'dashboard' and driver.page_source
    assert REQUIRED_FIELD_ERR in driver.page_source
    assert TOS_POLICIES_ERR in driver.page_source

# Test invalid register without checking agreement checkbox
def test_register_uncheck_checkbox(driver):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    CONF_PASSWORD = 'password'
    TOS_POLICIES_ERR = 'You must agree to the terms and policies to register!'

    # Enter credentials
    driver.find_element_by_id('username').send_keys(USERNAME)
    driver.find_element_by_id('password').send_keys(PASSWORD)
    driver.find_element_by_id('confirm_password').send_keys(CONF_PASSWORD)
    driver.find_element_by_id('submit').click()
    assert driver.current_url.split(sep='/')[-1] != 'dashboard'
    assert TOS_POLICIES_ERR in driver.page_source

# Test invalid register with mismatched passwords
def test_register_different_passwords(driver):
    PASSWORD = 'password'
    CONF_PASSWORD_ERR = 'password1'
    DIFF_PASSWORS_ERR = 'Password must match!'

    # Enter credentials
    driver.find_element_by_id('password').send_keys(PASSWORD)
    driver.find_element_by_id('confirm_password').send_keys(CONF_PASSWORD_ERR)
    # Use JavaScript to select checkbox
    checkbox = driver.find_element_by_css_selector("#agreement")
    driver.execute_script("arguments[0].click();", checkbox)
    driver.find_element_by_id('submit').click()
    assert driver.current_url.split(sep='/')[-1] != 'dashboard'
    assert DIFF_PASSWORS_ERR in driver.page_source

# Test valid register
def test_register(driver):
    PASSWORD = 'password'
    CONF_PASSWORD = 'password'

    # Enter credentials
    driver.find_element_by_id('password').send_keys(PASSWORD)
    driver.find_element_by_id('confirm_password').send_keys(CONF_PASSWORD)
    driver.find_element_by_id('submit').click()
    # Assert user is redirected to dashboard
    assert driver.current_url.split(sep='/')[-1] == 'dashboard'
    logout(driver)

# Test invalid register with existing username
def test_register_existing(driver):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    CONF_PASSWORD = 'password'
    EXISTING_USERNAME_ERR = 'Username already taken!'

    # Click 'Get Started'
    driver.find_element(By.XPATH, '//*[@id="home"]/div[1]/div[1]/div/div/a').click()
    assert driver.current_url.split(sep='/')[-1] == 'register'

    # Enter credentials
    driver.find_element_by_id('username').send_keys(USERNAME)
    driver.find_element_by_id('password').send_keys(PASSWORD)
    driver.find_element_by_id('confirm_password').send_keys(CONF_PASSWORD)
    # Use JavaScript to select checkbox
    checkbox = driver.find_element_by_css_selector("#agreement")
    driver.execute_script("arguments[0].click();", checkbox)
    driver.find_element_by_id('submit').click()
    assert driver.current_url.split(sep='/')[-1] != 'dashboard'
    assert EXISTING_USERNAME_ERR in driver.page_source


# Test logging in user from homepage - flows after logging out a newly registered user
# Test invalid login with unregistered account
def test_unregistered_login(driver):
    driver.get('http://localhost:5000')
    assert driver.title == 'Project Piscator'

    USERNAME = 'testuser123456'
    PASSWORD = 'password'
    INVALID_USER_PASS_ERR = 'Invalid username or password'

    login(driver, USERNAME, PASSWORD)

    assert driver.current_url.split(sep='/')[-1] != 'dashboard'
    assert INVALID_USER_PASS_ERR in driver.page_source

# Test invalid login with incorrect password
def test_invalid_password_login(driver):
    USERNAME = 'testuser123'
    PASSWORD = 'password123'
    INVALID_USER_PASS_ERR = 'Invalid username or password'

    driver.find_element_by_id('username').send_keys(USERNAME)
    driver.find_element_by_id('password').send_keys(PASSWORD)
    driver.find_element_by_id('submit').click()

    assert driver.current_url.split(sep='/')[-1] != 'dashboard'
    assert INVALID_USER_PASS_ERR in driver.page_source

# Test invalid login with empty password
def test_empty_password_login(driver):
    USERNAME = 'testuser123'

    driver.find_element_by_id('username').send_keys(USERNAME)
    driver.find_element_by_id('submit').click()

    assert driver.current_url.split(sep='/')[-1] != 'dashboard'

# Test valid login
def test_login(driver):
    PASSWORD = 'password'

    driver.find_element_by_id('password').send_keys(PASSWORD)
    driver.find_element_by_id('submit').click()

    # Assert user is redirected to dashboard
    assert driver.current_url.split(sep='/')[-1] == 'dashboard'
