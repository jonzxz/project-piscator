import pytest
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Clicks on 'Emails' in dashboard, assert url = dashboard/emails
# Clicks on 'Add New Email' and wait for Bootstrap modal to pop up
# Enters email credentials and assert new email is displayed in page
def test_add_email(driver):
    # Wait for navbar arrow to appear
    wait_nav_arrow = WebDriverWait(driver, 5)
    wait_nav_arrow.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/button')))
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/button').click()

    # Wait for subscription button to appear
    wait_subscription = WebDriverWait(driver, 3)
    wait_subscription.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mySidepanel"]/a[4]')))
    driver.find_element(By.XPATH, '//*[@id="mySidepanel"]/a[4]').click()
    # Assert redirected to /emails page
    assert driver.current_url.split(sep='/')[-1] == 'emails'

    # Add Email Button
    wait_mail_btn = WebDriverWait(driver, 3)
    wait_mail_btn.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/button')))
    driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/button').click()

    # Enter Add Email Address
    wait_email_field = WebDriverWait(driver, 3)
    wait_email_field.until(EC.visibility_of_element_located((By.ID, 'email_address')))
    driver.find_element_by_id('email_address').send_keys("testmail456@mymail.com")
    driver.find_element_by_id('password').send_keys("password1")
    driver.find_element_by_id('submit').click()
    assert 'testmail456@mymail.com' in driver.page_source

# Clicks on power button on added email
# Assert the "Active" column for added email is now "False"
def test_deactivate_email(driver):
    wait_email_entry = WebDriverWait(driver, 5)
    wait_email_entry.until(EC.visibility_of_element_located((By.NAME, 'activate-testmail456@mymail.com')))
    driver.find_element_by_name('activate-testmail456@mymail.com').click()
    assert driver.find_element_by_name('status-testmail456@mymail.com').text == 'Inactive'
