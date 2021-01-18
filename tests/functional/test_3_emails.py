import pytest
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from app.utils.FileUtils import get_server_mail_cred

# Flows after test_2_authentication's test_login
# Clicks on 'Emails' in dashboard, assert url = dashboard/emails
# Clicks on 'Add New Email' and wait for Bootstrap modal to pop up
# Enters email credentials and assert new email is displayed in page
def test_add_email(driver):
    MAIL_CREDS = get_server_mail_cred()
    EMAIL_ADDR = MAIL_CREDS[0]
    EMAIL_PASSWORD = MAIL_CREDS[1]

    # Wait for subscription button to appear and click
    wait_subscription = WebDriverWait(driver, 3)
    wait_subscription.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="user-panel"]/a[3]')))
    driver.find_element(By.XPATH, '//*[@id="user-panel"]/a[3]').click()
    # Assert redirected to /emails page
    assert driver.current_url.split(sep='/')[-1] == 'emails'

    # Wait for Add Email Button to appear and click
    wait_mail_btn = WebDriverWait(driver, 3)
    wait_mail_btn.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div/button[1]')))
    driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div/button[1]').click()

    # Wait for fields in modal to appear and click
    wait_email_field = WebDriverWait(driver, 3)
    wait_email_field.until(EC.visibility_of_element_located((By.ID, 'email_address')))
    driver.find_element_by_id('email_address').send_keys(EMAIL_ADDR)
    driver.find_element_by_id('password').send_keys(EMAIL_PASSWORD)
    driver.find_element_by_id('add_mail_submit').click()
    assert EMAIL_ADDR in driver.page_source

# Flows after test_add_email
# Clicks on "Clean Mailbox" to enter a phishing check
# Assert page redirected to Detection Results
# Goes back to Subscriptions page
def test_check_email(driver):
    MAIL_CREDS = get_server_mail_cred()
    EMAIL_ADDR = MAIL_CREDS[0]
    EMAIL_PASSWORD = MAIL_CREDS[1]

    sleep(2)
    wait_email_entry = WebDriverWait(driver, 5)
    wait_email_entry.until(EC.visibility_of_element_located((By.NAME, 'clean-{}'.format(EMAIL_ADDR))))
    driver.find_element_by_name('clean-{}'.format(EMAIL_ADDR)).click()
    assert driver.current_url.split(sep='/')[-2] == 'phish'
    assert 'Detection Results' in driver.page_source

    # Wait for subscription button to appear and click
    wait_subscription = WebDriverWait(driver, 3)
    wait_subscription.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="user-panel"]/a[3]')))
    driver.find_element(By.XPATH, '//*[@id="user-panel"]/a[3]').click()
    # Assert redirected to /emails page
    assert driver.current_url.split(sep='/')[-1] == 'emails'

# Flows after test_check_email
# Clicks on "Detection History" to view all history
# Assert page redirected to Detection History
# Goes back to Subscriptions page
def test_detection_history(driver):
    MAIL_CREDS = get_server_mail_cred()
    EMAIL_ADDR = MAIL_CREDS[0]

    sleep(2)
    wait_email_entry = WebDriverWait(driver, 5)
    wait_email_entry.until(EC.visibility_of_element_located((By.NAME, 'history-{}'.format(EMAIL_ADDR))))
    driver.find_element_by_name('history-{}'.format(EMAIL_ADDR)).click()
    assert driver.current_url.split(sep='/')[-2] == 'history'
    assert 'Detection History' in driver.page_source

    # Wait for subscription button to appear and click
    wait_subscription = WebDriverWait(driver, 3)
    wait_subscription.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="user-panel"]/a[3]')))
    driver.find_element(By.XPATH, '//*[@id="user-panel"]/a[3]').click()
    # Assert redirected to /emails page
    assert driver.current_url.split(sep='/')[-1] == 'emails'


# Flows after test_add_email
# Clicks on power button on added email by using element name-<email>
# Assert the "Active" column for added email is now "False" using element status-<email>
def test_deactivate_email(driver):
    MAIL_CREDS = get_server_mail_cred()
    EMAIL_ADDR = MAIL_CREDS[0]

    sleep(2)
    wait_email_entry = WebDriverWait(driver, 5)
    wait_email_entry.until(EC.visibility_of_element_located((By.NAME, 'activate-{}'.format(EMAIL_ADDR))))
    driver.find_element_by_name('activate-{}'.format(EMAIL_ADDR)).click()
    assert driver.find_element_by_name('status-{}'.format(EMAIL_ADDR)).text == 'Inactive'
