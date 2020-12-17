import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .test_2_authentication import login, logout
from time import sleep

def test_change_password(driver):
    # Wait for navbar arrow to appear
    wait_nav_arrow = WebDriverWait(driver, 5)
    wait_nav_arrow.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/button')))
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/button').click()

    # Wait for account settings button to appear
    wait_acc_set_btn = WebDriverWait(driver, 3)
    wait_acc_set_btn.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mySidepanel"]/a[5]')))
    driver.find_element(By.XPATH, '//*[@id="mySidepanel"]/a[5]').click()
    # Assert redirected to /account page
    assert driver.current_url.split(sep='/')[-1] == 'account'

    wait_update_btn = WebDriverWait(driver, 5)
    wait_update_btn.until(EC.visibility_of_element_located((By.ID, 'submit')))
    driver.find_element_by_id('current_password').send_keys('password')
    driver.find_element_by_id('new_password').send_keys('newpassword')
    driver.find_element_by_id('confirm_new_password').send_keys('newpassword')
    driver.find_element_by_id('submit').click()

    logout(driver)
    assert driver.current_url.split(sep='/')[-1] == 'index'

    login(driver, 'testuser123', 'newpassword')
    assert driver.current_url.split(sep='/')[-1] == 'dashboard'

# def test_disable_account(driver):
#     # Wait for navbar arrow to appear
#     wait_nav_arrow = WebDriverWait(driver, 5)
#     wait_nav_arrow.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/button')))
#     driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/button').click()
#
#     # Wait for account settings button to appear
#     wait_acc_set_btn = WebDriverWait(driver, 3)
#     wait_acc_set_btn.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mySidepanel"]/a[5]')))
#     driver.find_element(By.XPATH, '//*[@id="mySidepanel"]/a[5]').click()
#     # Assert redirected to /account page
#     assert driver.current_url.split(sep='/')[-1] == 'account'
#
#     wait_update_btn = WebDriverWait(driver, 5)
#     wait_update_btn.until(EC.visibility_of_element_located((By.ID, 'submit')))
#     driver.find_element_by_id('current_password').send_keys('newpassword')
#     wait_disable_btn = WebDriverWait(driver, 5)
#     wait_disable_btn.until(EC.visibility_of_element_located((By.ID, 'disable_acc_switch')))
#     driver.execute_script("arguments[0].click();", wait_disable_btn)
#     driver.find_element_by_id('submit').click()
#
#     logout(driver)
#
#     login(driver, 'testuser123', 'newpassword')
#     assert not driver.current_url.split(sep='/')[-1] == 'dashboard'
