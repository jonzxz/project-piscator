import pytest
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Clicks on 'Get Started', enter register credentials and check user is redirected to dashboard
# Finally logs out
def test_register(driver):
    # Click 'Get Started'
    driver.find_element(By.XPATH, '//*[@id="home"]/div[1]/div[1]/div/div/a').click()
    assert driver.current_url.split(sep='/')[-1] == 'register'
    # Enter credentials
    driver.find_element_by_id('username').send_keys("testuser123")
    driver.find_element_by_id('password').send_keys("password")
    driver.find_element_by_id('confirm_password').send_keys("password")
    driver.find_element_by_id('submit').click()
    # Assert user is redirected to dashboard
    assert driver.current_url.split(sep='/')[-1] == 'dashboard'
    user_logout(driver)

# Clicks on 'Sign In', enter login credentials and check user is redirected to dashboard
def test_login(driver):
    # Click 'Sign In'
    wait_login_btn = WebDriverWait(driver, 5)
    wait_login_btn.until(EC.visibility_of_element_located((By.XPATH, '/html/body/header/div[1]/div/div/div/nav/div[2]/a')))
    driver.find_element(By.XPATH, '/html/body/header/div[1]/div/div/div/nav/div[2]/a').click()
    assert driver.current_url.split(sep='/')[-1] == 'login'
    # Enter credentials
    driver.find_element_by_id('username').send_keys("testuser123")
    driver.find_element_by_id('password').send_keys("password")
    driver.find_element_by_id('submit').click()
    # Assert user is redirected to dashboard
    assert driver.current_url.split(sep='/')[-1] == 'dashboard'

def user_logout(driver):
    # Logout
    wait_nav_arrow = WebDriverWait(driver, 5)
    wait_nav_arrow.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/button')))
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/button').click()
    wait_logout = WebDriverWait(driver, 5)
    wait_logout.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mySidepanel"]/a[6]')))
    driver.find_element(By.XPATH, '//*[@id="mySidepanel"]/a[6]').click()
