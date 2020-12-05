import pytest

# Test successful connection to localhost:5000 and display project homepage
def test_homepage(driver):
    assert driver.title == 'Project Piscator'
