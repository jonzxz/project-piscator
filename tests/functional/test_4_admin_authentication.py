import pytest
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Clicks on 'Sign In', enter login credentials and check admin is redirected to admin dashboard
def test_login(driver):
    # Click 'Sign In'
    driver.find_element(By.XPATH, '/html/body/header/div[1]/div/div/div/nav/div[2]/a').click()
    assert driver.current_url.split(sep='/')[-1] == 'login'
    # Enter credentials
    driver.find_element_by_id('username').send_keys("admin")
    driver.find_element_by_id('password').send_keys("password")
    driver.find_element_by_id('submit').click()
    # Assert user is redirected to admin dashboard
    # [-2] due to /admin/
    assert driver.current_url.split(sep='/')[-2] == 'admin'
    # Logout
    wait_logout = WebDriverWait(driver, 5)
    wait_logout.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mySidepanel"]/a[5]')))
    driver.find_element(By.XPATH, '//*[@id="mySidepanel"]/a[5]').click()
