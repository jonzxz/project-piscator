import pytest
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Clicks on 'Emails' in dashboard, assert url = dashboard/emails
# Clicks on 'Add New Email' and wait for Bootstrap modal to pop up
# Enters email credentials and assert new email is displayed in page
def test_add_email(driver):
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/a[3]').click()
    assert driver.current_url.split(sep='/')[-1] == 'emails'
    driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/button').click()
    wait = WebDriverWait(driver, 5)
    wait.until(EC.visibility_of_element_located((By.ID, 'email_address')))
    driver.find_element_by_id('email_address').send_keys("testmail456@mymail.com")
    driver.find_element_by_id('password').send_keys("password1")
    driver.find_element_by_id('submit').click()
    sleep(5)
    assert 'testmail456@mymail.com' in driver.page_source

# Clicks on power button on added email
# Assert the "Active" column for added email is now "False"
def test_deactivate_email(driver):
    driver.find_element_by_name('activate-testmail456@mymail.com').click()
    assert driver.find_element_by_name('status-testmail456@mymail.com').text == 'False'
    sleep(5)
