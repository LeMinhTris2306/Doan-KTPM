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

# ============= Test các chức năng đăng nhập của user =============

#Test đăng nhập thành công
#passed in 11.79s
def test_valid_login(driver):
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
    driver.find_element(By.NAME, "email").send_keys("lmt@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("lmt123")
    
    login_button = get_clickable_element(driver, By.XPATH, "//form//button")
    login_button.click()
    time.sleep(1)
    current_url = driver.current_url
    assert "http://localhost/mongodb/index.php" in current_url

# Test đăng nhập sai mật khẩu
#passed in 10.66s
def test_login_with_wrong_password(driver):
        #Kết nối đến web
    driver.get("http://localhost/mongodb/")

    #Chọn nút đăng nhập
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    time.sleep(0.5)
    login_button = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a//div//button")
    login_button.click()
    time.sleep(1)
    #Điền thông tin và đăng nhập
    driver.find_element(By.NAME, "email").send_keys("lmt@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123lmt")
    login_button = get_clickable_element(driver, By.XPATH, "//form//button")
    #Nhấn đăng nhập
    login_button.click()
    time.sleep(1)
    message = driver.find_element(By.XPATH, "//div[@class='container']/form/a").text
    assert "Incorect!" in message

# Test đăng nhập khi để trống thông tin
# passed in 10.58s
def test_login_with_blank_fields(driver):
        #Kết nối đến web
    driver.get("http://localhost/mongodb/")

    #Chọn nút đăng nhập
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    time.sleep(0.5)
    login_button = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a//div//button")
    login_button.click()
    time.sleep(1)
    #Điền thông tin và đăng nhập
    driver.find_element(By.NAME, "email").send_keys("")
    driver.find_element(By.NAME, "password").send_keys("")
    
    login_button = get_clickable_element(driver, By.XPATH, "//form//button")
    #Nhấn đăng nhập
    login_button.click()
    time.sleep(1)
    message = driver.find_element(By.XPATH, "//div[@class='container']/form/a").text
    assert "Không được để trống Email" in message

# Test đăng nhập khi để trống mật khẩu
# passed in 10.62s
def test_login_with_blank_password_field(driver):
        #Kết nối đến web
    driver.get("http://localhost/mongodb/")

    #Chọn nút đăng nhập
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    time.sleep(0.5)
    login_button = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a//div//button")
    login_button.click()
    time.sleep(1)
    #Điền thông tin và đăng nhập
    driver.find_element(By.NAME, "email").send_keys("lmt@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("")
    login_button = get_clickable_element(driver, By.XPATH, "//form//button")
    #Nhấn đăng nhập
    login_button.click()
    time.sleep(1)
    message = driver.find_element(By.XPATH, "//div[@class='container']/form/a").text
    assert "Không được để trống tài khoản" in message

# Test đăng nhập khi điền email không đúng
# passed in 10.63s
def test_login_with_wrong_email(driver):
    #Kết nối đến web
    driver.get("http://localhost/mongodb/")

    #Chọn nút đăng nhập
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    time.sleep(0.5)
    login_button = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a//div//button")
    login_button.click()
    time.sleep(1)
    #Điền thông tin và đăng nhập
    driver.find_element(By.NAME, "email").send_keys("lmt")
    driver.find_element(By.NAME, "password").send_keys("lmt123")
    login_button = get_clickable_element(driver, By.XPATH, "//form//button")
    #Nhấn đăng nhập
    login_button.click()
    time.sleep(1)
    message = driver.find_element(By.XPATH, "//div[@class='container']/form/a").text
    assert "Incorect!" in message

#Test đăng nhập bằng tài khoản đã bị khóa
#Test fail vì vẫn đăng nhập được
def test_login_with_banned_account(driver):
    #Kết nối đến web
    driver.get("http://localhost/mongodb/")

    #Chọn nút đăng nhập
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    time.sleep(0.5)
    login_button = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a//div//button")
    login_button.click()
    time.sleep(1)
    #Điền thông tin và đăng nhập
    driver.find_element(By.NAME, "email").send_keys("lmtt@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("lmt123")
    login_button = get_clickable_element(driver, By.XPATH, "//form//button")
    #Nhấn đăng nhập
    login_button.click()
    time.sleep(1)
    message = driver.find_element(By.XPATH, "//div[@class='container']/form/a").text
    assert "Tài khoản của bạn đã bị khoá!" in message

# Test nosql injection
# passed in 10.74s
def test_nosql_injection(driver):
        #Kết nối đến web
    driver.get("http://localhost/mongodb/")

    #Chọn nút đăng nhập
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    time.sleep(0.5)
    login_button = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a//div//button")
    login_button.click()
    time.sleep(1)
    #Điền thông tin và đăng nhập
    driver.find_element(By.NAME, "email").send_keys(f"'; return '' == '")
    driver.find_element(By.NAME, "password").send_keys("lmt123")
    login_button = get_clickable_element(driver, By.XPATH, "//form//button")
    #Nhấn đăng nhập
    login_button.click()
    time.sleep(1)
    message = driver.find_element(By.XPATH, "//div[@class='container']/form/a").text
    assert "Incorect!" in message

#Test chức năng đăng xuất
# passed in 13.74s
def test_logout(driver):
    #Thực hiện đăng nhập thành công
    test_valid_login(driver)
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    time.sleep(0.5)
    #Ấn nút đăng xuất
    logout_button = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a//div//button")
    logout_button.click()
    time.sleep(1)
    #Sau khi đăng xuất thì trở lại trang chủ để kiểm tra
    return_to_homepage = get_clickable_element(driver, By.XPATH, "//a[text()='quay lại trang chủ']")
    return_to_homepage.click()
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    message = driver.find_element(By.XPATH, "//div[@class='login-logout-popup']//p").text
    assert "Chưa Đăng Nhập" in message

#Test chức năng tìm kiếm khi để trống
# passed in 10.01s
def test_find_product_with_blank_field(driver):
        #Kết nối đến web
    driver.get("http://localhost/mongodb/")
    time.sleep(1)
    #Nhập thông tin tìm kiếm
    driver.find_element(By.NAME, "timkiem").send_keys("")
    search_btn = get_clickable_element(driver, By.XPATH, "//button[text()='Tìm kiếm']")
    search_btn.click()
    time.sleep(1)
    
    #Tìm kiếm kết quả
    message = driver.find_element(By.XPATH, "//body").text
    assert "Vui lòng nhập từ khóa tìm kiếm." in message

#Test chức năng tìm kiếm sản phẩm không tồn tại
# passed in 11.16s
def test_find_product_that_not_exist(driver):
    #Kết nối đến web
    driver.get("http://localhost/mongodb/")
    time.sleep(1)
    #Nhập thông tin tìm kiếm
    driver.find_element(By.NAME, "timkiem").send_keys("Album")
    search_btn = get_clickable_element(driver, By.XPATH, "//button[text()='Tìm kiếm']")
    search_btn.click()
    time.sleep(1)
    
    #Tìm kiếm kết quả
    message = driver.find_element(By.XPATH, "//h3").text
    time.sleep(1)
    assert "Không tìm thấy sách." in message

#Test chức năng tìm kiếm đúng sách
# passed in 13.09s
def test_find_speciic_product(driver):
        #Kết nối đến web
    driver.get("http://localhost/mongodb/")
    time.sleep(1)
    #Nhập thông tin tìm kiếm
    driver.find_element(By.NAME, "timkiem").send_keys("Sách lập trình python")
    time.sleep(1)
    search_btn = get_clickable_element(driver, By.XPATH, "//button[text()='Tìm kiếm']")
    search_btn.click()
    time.sleep(2)
    
    #Tìm kiếm kết quả
    book_name = driver.find_element(By.XPATH, "//div[@class='product-card']").text
    time.sleep(1)
    assert "SÁCH LẬP TRÌNH PYTHON" in book_name

#Test chức năng tìm kiếm bằng 1 phần của tên sản phẩm đúng
# passed in 13.03s
def test_find_product_with_keyword(driver):
    keyword = "sách"
    #Kết nối đến web
    driver.get("http://localhost/mongodb/")
    time.sleep(1)
    #Nhập thông tin tìm kiếm
    driver.find_element(By.NAME, "timkiem").send_keys(keyword)
    time.sleep(1)
    search_btn = get_clickable_element(driver, By.XPATH, "//button[text()='Tìm kiếm']")
    search_btn.click()
    time.sleep(2)
    
    #Tìm kiếm kết quả
    elements = driver.find_elements(By.XPATH, "//div[@class='product-card']")
    time.sleep(1)
    book_names = list(map(lambda element: element.text, elements))
    for book_name in book_names:
        assert keyword.upper() in book_name

#Test chức năng tìm kiếm sách bị ẩn
#Fail vì các sách ẩn vẫn hiển thị
def test_find_hidden_product(driver):
    keyword = "TEST"
    #Kết nối đến web
    driver.get("http://localhost/mongodb/")
    time.sleep(1)
    #Nhập thông tin tìm kiếm
    driver.find_element(By.NAME, "timkiem").send_keys(keyword)
    time.sleep(1)
    search_btn = get_clickable_element(driver, By.XPATH, "//button[text()='Tìm kiếm']")
    search_btn.click()
    time.sleep(2)
    
    #Tìm kiếm kết quả
    books = driver.find_elements(By.XPATH, "//div[@class='product-card']")
    time.sleep(1)
    #Kiểm tra testcase
    if len(books) == 0:
        message = driver.find_element(By.XPATH, "//h3").text
        assert "Không tìm thấy sách." in message
    for book_name in books:
        assert keyword.upper() not in book_name.text

#Test chức năng lọc theo thể loại
# passed in 14.25s
def test_product_type_filter(driver):
    #Kết nối đến web
    driver.get("http://localhost/mongodb/")
    time.sleep(1)

    categories = driver.find_elements(By.XPATH, "//select[@name='ma_the_loai']//option")
    for i in range(1, len(categories)):
        option = get_clickable_element(driver, By.XPATH, "//select[@name='ma_the_loai']")
        option.click()
        option.send_keys(Keys.DOWN)
        option.click()
        books = driver.find_elements(By.XPATH, "//div[@class='product-card']")
        assert len(books) > 0
        time.sleep(1)

