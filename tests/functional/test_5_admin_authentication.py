import pytest
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .test_2_authentication import login, logout

# Flows from test_4_user disable_account
# Disabled user is stays at login page, .get to go back to homepage
# Test logging in to admin account and redirection to admin dashboard
def test_admin_login(driver):
    ADMIN_USER = 'admin'
    PASSWORD = 'password'
    driver.get('http://localhost:5000')
    # Enter credentials
    login(driver, ADMIN_USER, PASSWORD)
    # Assert user is redirected to admin dashboard
    # [-2] due to /admin/
    assert driver.current_url.split(sep='/')[-2] == 'admin'

# Flows from admin login
# Test opening the user view and that redirection is correct and User table is present
# -- Possible improvement to check if created TESTUSER123 is present
def test_admin_can_view_users(driver):
    # Wait for User button to appear and click
    wait_user_btn = WebDriverWait(driver, 3)
    wait_user_btn.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="admin-panel"]/a[2]')))
    driver.find_element(By.XPATH, '//*[@id="admin-panel"]/a[2]').click()

    # Assert redirected to admin/user page
    # Assert table that populates database info is present
    assert '/'.join(driver.current_url.split(sep='/')[-3:]) == 'admin/user/'
    assert driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[1]/table')

# Flows from test_admin_can_view_users
# Logs out admin from administrative dashboard and return to index
def test_admin_logout(driver):
    # Logout
    wait_logout = WebDriverWait(driver, 5)
    wait_logout.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="admin-panel"]/a[5]')))
    driver.find_element(By.XPATH, '//*[@id="admin-panel"]/a[5]').click()

    # Assert redirected to index
    assert driver.current_url.split(sep='/')[-1] == 'index'
