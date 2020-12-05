import pytest
import sys
from selenium.webdriver.common.by import By
from time import sleep

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
    # Logout
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/a[5]').click()

# Clicks on 'Sign In', enter login credentials and check user is redirected to dashboard
def test_login(driver):
    # Click 'Sign In'
    driver.find_element(By.XPATH, '/html/body/header/div[1]/div/div/div/nav/div[2]/a').click()
    assert driver.current_url.split(sep='/')[-1] == 'login'
    # Enter credentials
    driver.find_element_by_id('username').send_keys("testuser123")
    driver.find_element_by_id('password').send_keys("password")
    driver.find_element_by_id('submit').click()
    # Assert user is redirected to dashboard
    assert driver.current_url.split(sep='/')[-1] == 'dashboard'
    sleep(2)
