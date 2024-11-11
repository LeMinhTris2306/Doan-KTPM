import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    prefs = {
        'autofill.profile_enabled': False
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

def get_clickable_element(driver, by: By, arg, timeout = 10):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, arg))
    )
    return element

#Test đăng nhập bằng tài khoản admin
def testcase_1(driver):
    #Kết nối đến web
    driver.get("http://localhost/mongodb/")
    time.sleep(1)
    #Chọn nút đăng nhập
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    time.sleep(0.5)
    login_button = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a//div//button")
    login_button.click()
    time.sleep(1)
    #Điền thông tin và đăng nhập
    driver.find_element(By.NAME, "email").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("123")
    
    login_button = get_clickable_element(driver, By.XPATH, "//form//button")
    login_button.click()
    time.sleep(1)
    current_url = driver.current_url
    assert "http://localhost/mongodb/checkin.php" in current_url

#Test đăng xuất khỏi trang admin
def testcase_2(driver):
    #Đăng nhập vào trang admin
    testcase_1(driver)
    #Ấn nút đăng xuất
    logout_btn = get_clickable_element(driver, By.XPATH, "//form[@action='logout.php']/button")
    logout_btn.click()

#Test điều hướng sang trang quản lý user
def testcase_3(driver):
    testcase_1(driver)

    user_nav = get_clickable_element(driver, By.XPATH, "//div[@class='nav-space']/p[text()='Quản lý tài khoản']")
    user_nav.click()

    assert "http://localhost/mongodb/user.php" in driver.current_url