import pytest
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Flows after test_2_authentication's test_login
# Clicks on 'Emails' in dashboard, assert url = dashboard/emails
# Clicks on 'Add New Email' and wait for Bootstrap modal to pop up
# Enters email credentials and assert new email is displayed in page
def test_add_email(driver):
    EMAIL_ADDR = 'testmail456@mymail.com'
    EMAIL_PASSWORD = 'password1'
    # Wait for navbar arrow to appear and click
    wait_nav_arrow = WebDriverWait(driver, 5)
    wait_nav_arrow.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/button')))
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/button').click()

    # Wait for subscription button to appear and click
    wait_subscription = WebDriverWait(driver, 3)
    wait_subscription.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mySidepanel"]/a[4]')))
    driver.find_element(By.XPATH, '//*[@id="mySidepanel"]/a[4]').click()
    # Assert redirected to /emails page
    assert driver.current_url.split(sep='/')[-1] == 'emails'

    # Wait for Add Email Button to appear and click
    wait_mail_btn = WebDriverWait(driver, 3)
    wait_mail_btn.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/button')))
    driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/button').click()

    # Wait for fields in modal to appear and click
    wait_email_field = WebDriverWait(driver, 3)
    wait_email_field.until(EC.visibility_of_element_located((By.ID, 'email_address')))
    driver.find_element_by_id('email_address').send_keys(EMAIL_ADDR)
    driver.find_element_by_id('password').send_keys(EMAIL_PASSWORD)
    driver.find_element_by_id('submit').click()
    assert EMAIL_ADDR in driver.page_source

# Flows after test_add_email
# Clicks on power button on added email by using element name-<email> 
# Assert the "Active" column for added email is now "False" using element status-<email>
def test_deactivate_email(driver):
    EMAIL_ADDR = 'testmail456@mymail.com'
    wait_email_entry = WebDriverWait(driver, 5)
    wait_email_entry.until(EC.visibility_of_element_located((By.NAME, 'activate-{}'.format(EMAIL_ADDR))))
    driver.find_element_by_name('activate-{}'.format(EMAIL_ADDR)).click()
    assert driver.find_element_by_name('status-{}'.format(EMAIL_ADDR)).text == 'Inactive'
