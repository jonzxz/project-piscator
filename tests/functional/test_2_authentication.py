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
    wait_login_btn.until(EC.visibility_of_element_located((By.XPATH, '/html/body/header/div[1]/div/div/div/nav/div[2]/a')))
    driver.find_element(By.XPATH, '/html/body/header/div[1]/div/div/div/nav/div[2]/a').click()
    # Enter credentials
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('submit').click()

# Reusable function to provide USER logout automation from dashboard
# clicks the nav bar arrow and clicks sign out
def logout(driver):
    # Waits for navbar arrow to appear and click
    wait_nav_arrow = WebDriverWait(driver, 5)
    wait_nav_arrow.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/button')))
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/button').click()
    # Waits for logout button to appear and click
    wait_logout = WebDriverWait(driver, 5)
    wait_logout.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mySidepanel"]/a[6]')))
    driver.find_element(By.XPATH, '//*[@id="mySidepanel"]/a[6]').click()

# Test registering a user from homepage
# Clicks on 'Get Started', enter register credentials and check user is redirected to dashboard
# Finally logs out
def test_register(driver):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    CONF_PASSWORD = 'password'
    # Click 'Get Started'
    driver.find_element(By.XPATH, '//*[@id="home"]/div[1]/div[1]/div/div/a').click()
    assert driver.current_url.split(sep='/')[-1] == 'register'
    # Enter credentials
    driver.find_element_by_id('username').send_keys(USERNAME)
    driver.find_element_by_id('password').send_keys(PASSWORD)
    driver.find_element_by_id('confirm_password').send_keys(CONF_PASSWORD)
    driver.find_element_by_id('submit').click()
    # Assert user is redirected to dashboard
    assert driver.current_url.split(sep='/')[-1] == 'dashboard'
    logout(driver)

# Test logging in user from homepage - flows after logging out a newly registered user
# Uses login utility function
def test_login(driver):
    USERNAME = 'testuser123'
    PASSWORD = 'password'
    login(driver, USERNAME, PASSWORD)
    # Assert user is redirected to dashboard
    assert driver.current_url.split(sep='/')[-1] == 'dashboard'
