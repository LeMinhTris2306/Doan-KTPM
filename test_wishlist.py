import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from random import randint
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


#Test đăng nhập thành công
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
    driver.find_element(By.NAME, "email").send_keys("lmt2@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("lmt123")
    
    login_button = get_clickable_element(driver, By.XPATH, "//form//button")
    login_button.click()
    time.sleep(1)
    current_url = driver.current_url
    assert "http://localhost/mongodb/index.php" in current_url

#Test thêm vào wishlist
# passed in 19.36s
def test_add_to_wishlist(driver):
    test_valid_login(driver)

    #Bấm nút page down để kéo xuống
    driver.find_element(By.XPATH, "//body").send_keys(Keys.PAGE_DOWN)
    driver.find_element(By.XPATH, "//body").send_keys(Keys.PAGE_DOWN)
    #đợi cho các element load
    time.sleep(0.4)
    #chọn 1 cuốn sách và bấm vào
    index = randint(1, 5)
    book = get_clickable_element(driver, By.XPATH, f"/html/body/section[2]/div/div[{index}]")
    book.click()
    time.sleep(1)
    book_name = driver.find_element(By.XPATH, "/html/body/section/div/h2").text
    #Thêm sách vào wishlist
    add_to_wishlist = get_clickable_element(driver, By.XPATH, "/html/body/section/div/div/form[2]/button")
    add_to_wishlist.click()
    time.sleep(1)
    #Kiểm tra là sách có được thêm vào wishlist chưa
    #Lấy danh sách sản phẩm trong wishlist
    books = driver.find_elements(By.XPATH, "//div[@class='cart-info']/div/h3")
    #Lấy tên
    book_names = list(map(lambda book: str(book.text).lower(), books))
    time.sleep(1)
    assert str(book_name).lower() in book_names

#Test thêm nhiều sách vào wishlist
# passed in 21.33s
def test_add_multi_pd_to_wishlist(driver, no_products = 2):
    count = 0
    test_valid_login(driver)
    added_book_names = []
    index = randint(1, 5)
    while count < no_products:
        #Bấm nút page down để kéo xuống
        driver.find_element(By.XPATH, "//body").send_keys(Keys.PAGE_DOWN)
        driver.find_element(By.XPATH, "//body").send_keys(Keys.PAGE_DOWN)
        #đợi cho các element load
        time.sleep(0.4)
        book = get_clickable_element(driver, By.XPATH, f"/html/body/section[2]/div/div[{index}]")
        book.click()
        time.sleep(1)
        book_name = driver.find_element(By.XPATH, "/html/body/section/div/h2").text
        added_book_names.append(str(book_name).lower())
        #Thêm sách vào wishlist
        add_to_wishlist = get_clickable_element(driver, By.XPATH, "/html/body/section/div/div/form[2]/button")
        add_to_wishlist.click()
        time.sleep(1)
        #Về trang chủ
        count += 1
        if count < no_products:
            homepage_btn = get_clickable_element(driver, By.XPATH, "/html/body/ul/li[1]/a")
            homepage_btn.click()
            index = index - 1 if index > 1 else 5

    #Kiểm tra là sách có được thêm vào wishlist chưa
    #Lấy danh sách sản phẩm trong wishlist
    driver.find_element(By.XPATH, "//body").send_keys(Keys.END)
    books = driver.find_elements(By.XPATH, "//div[@class='cart-info']/div/h3")
    #Lấy tên
    book_names = list(map(lambda book: str(book.text).lower(), books))
    time.sleep(1)
    result = [added_book_name in book_names for added_book_name in added_book_names]
    assert False not in result

#test Xem chi tiết sách trong wishlist
# passed in 17.50s
def test_book_detail_in_wishlist(driver, add_new=True):
    if add_new:
        test_add_to_wishlist(driver)

    book_name = driver.find_element(By.XPATH, "//div[@class='cart-info']/div/h3").text
    detail_btn = get_clickable_element(driver, By.XPATH, "//a[@class='link-text']")
    detail_btn.click()
    time.sleep(0.5)
    book_name_detail = driver.find_element(By.XPATH, "/html/body/section/div/h2").text

    assert str(book_name).lower() in str(book_name_detail).lower()

#Test Thêm 1 sách đã có trong wishlist
# passed in 19.54s
def test_add_existing_book_in_wishlist(driver):
    test_book_detail_in_wishlist(driver)

    add_to_wishlist = get_clickable_element(driver, By.XPATH, "/html/body/section/div/div/form[2]/button")
    add_to_wishlist.click()
    time.sleep(1)

    message = driver.find_element(By.XPATH, "/html/body/div[2]/h1[2]/a[3]/p").text
    assert "Bạn đã chọn sách này rồi" in message

#Test xóa 1 sản phẩm khỏi wishlist
# passed in 19.12s
def test_delete_from_wishlist(driver):
    #Thêm 1 sản phẩm vào wishlist trong trường hợp wishlist trống
    test_add_to_wishlist(driver)

    #Lấy tên sản phẩm đầu tiên để check
    book_name = driver.find_element(By.XPATH, "//div[@class='cart-info']/div/h3").text

    #xóa sản phẩm
    delete_btn = get_clickable_element(driver, By.NAME, "btn_remove")
    delete_btn.click()
    time.sleep(1)

    #Kiểm tra xem sản phẩm đã bị xóa khỏi wishlist chưa
    books = driver.find_elements(By.XPATH, "//div[@class='cart-info']/div/h3")
    #Lấy tên
    book_names = list(map(lambda book: str(book.text).lower(), books))
    time.sleep(1)
    assert str(book_name).lower() not in book_names

#test xóa tất cả sản phẩm trong wishlist sau khi thêm sản phẩm
# passed in 22.51s
def test_delete_all(driver):
    test_add_multi_pd_to_wishlist(driver)

    no_books = driver.find_elements(By.NAME, "btn_remove")
    for i in range(0, len(no_books)):
        dlt_btn = get_clickable_element(driver, By.NAME, "btn_remove")
        dlt_btn.click()
        time.sleep(0.2)

    a = driver.find_elements(By.XPATH, "/html/body/div[2]/h1[2]/table/tbody/tr")
    assert len(a) == 1

#Test thêm vào cart từ wishlist
# passed in 18.68s
def test_add_to_cart_form_wishlist(driver):
    test_add_to_wishlist(driver)

    #Lấy tên sản phẩm đầu tiên để check
    book_name = driver.find_element(By.XPATH, "//div[@class='cart-info']/div/h3").text

    add_to_cart_btn = get_clickable_element(driver, By.NAME, "addToCart")
    add_to_cart_btn.click()

    time.sleep(1)

    #Kiểm tra sản phẩm được thêm vào cart chưas
    books = driver.find_elements(By.XPATH, "//div[@class='cart-info']/div/h3")
    #Lấy tên
    book_names = list(map(lambda book: str(book.text).lower(), books))
    time.sleep(1)
    assert str(book_name).lower() in book_names