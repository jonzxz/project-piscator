import pytest
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .test_2_authentication import login, logout

# Clicks on 'Sign In', enter login credentials and check admin is redirected to admin dashboard
# Test ends with logging out the session
def test_admin_login(driver):
    # Enter credentials
    login(driver, 'admin', 'password')
    # Assert user is redirected to admin dashboard
    # [-2] due to /admin/
    assert driver.current_url.split(sep='/')[-2] == 'admin'

def test_admin_can_view_users(driver):
    # Wait for account settings button to appear
    wait_user_btn = WebDriverWait(driver, 3)
    wait_user_btn.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mySidepanel"]/a[2]')))
    driver.find_element(By.XPATH, '//*[@id="mySidepanel"]/a[2]').click()
    # Assert redirected to admin/user page
    assert '/'.join(driver.current_url.split(sep='/')[-3:]) == 'admin/user/'
    assert driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div/table')

def test_admin_logout(driver):
    # Logout
    wait_logout = WebDriverWait(driver, 5)
    wait_logout.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mySidepanel"]/a[5]')))
    driver.find_element(By.XPATH, '//*[@id="mySidepanel"]/a[5]').click()
    assert driver.current_url.split(sep='/')[-1] == 'index'
