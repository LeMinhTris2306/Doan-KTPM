import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
from random import randint

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

#Test chức năng hiển thị user
def testcase_3(driver):
    testcase_1(driver)

    user_nav = get_clickable_element(driver, By.XPATH, "//div[@class='nav-space']/p[text()='Quản lý tài khoản']")
    user_nav.click()

    assert "http://localhost/mongodb/user.php" in driver.current_url

#Test bộ lọc user
#Test nếu input rỗng
def testcase_4_empty_input(driver):
    testcase_3(driver)

    keyword = ""
    #Nhập keyword và ấn nút tìm kiếm
    driver.find_element(By.XPATH, "//input[@name='value_search']").send_keys(keyword)
    search_btn = get_clickable_element(driver, By.XPATH, "//button[text()='⚲ Tìm kiếm']")
    search_btn.click()
    #Đợi kết quả
    time.sleep(2)
    #Lấy kết quả
    results = driver.find_elements(By.XPATH, "//table/tbody//tr")
    #Vì keyword rỗng nên kq phải trả về toàn bộ user, len>1 vì element đầu tiên là header nên không tính
    assert len(results) > 1

#Test bằng 1 email cụ thể
def testcase_4_valid_email_input(driver, keyword=None):
    testcase_3(driver)

    cur_keyword = keyword if keyword else "lmt2@gmail.com"
    #Nhập keyword và ấn nút tìm kiếm
    driver.find_element(By.XPATH, "//input[@name='value_search']").send_keys(cur_keyword)
    search_btn = get_clickable_element(driver, By.XPATH, "//button[text()='⚲ Tìm kiếm']")
    search_btn.click()
    #Đợi kết quả
    time.sleep(2)
    #Lấy kết quả
    results = driver.find_elements(By.XPATH, "//table/tbody//tr//td[1]")
    #dùng lower vì phần hiển thị email luôn viết hoa chữ cái đầu
    #Lấy phần tử thứ 1 vì 0 là header
    assert cur_keyword in str(results[0].text).lower()

#Test bằng 1 phần email
def testcase_4_unfinished_input(driver):
    testcase_3(driver)

    keyword = "lmt"
    #Nhập keyword và ấn nút tìm kiếm
    driver.find_element(By.XPATH, "//input[@name='value_search']").send_keys(keyword)
    search_btn = get_clickable_element(driver, By.XPATH, "//button[text()='⚲ Tìm kiếm']")
    search_btn.click()
    #Đợi kết quả
    time.sleep(2)
    #Lấy kết quả
    results = driver.find_elements(By.XPATH, "//table/tbody//tr//td[1]")
    #dùng lower vì phần hiển thị email luôn viết hoa chữ cái đầu
    #Lấy phần tử thứ 1 vì 0 là header
    for i in range(1, len(results)):
        current_user = str(results[i].text).lower()
        assert keyword in current_user

#Test bằng 1 email không tồn tại
def testcase_4_invalid_email(driver):
    testcase_3(driver)

    #email chưa được đăng ký trong db
    keyword = "asdlmt123987@gmail.com"
    #Nhập keyword và ấn nút tìm kiếm
    driver.find_element(By.XPATH, "//input[@name='value_search']").send_keys(keyword)
    search_btn = get_clickable_element(driver, By.XPATH, "//button[text()='⚲ Tìm kiếm']")
    search_btn.click()
    #Đợi kết quả
    time.sleep(2)
    #Lấy kết quả
    results = driver.find_elements(By.XPATH, "//table/tbody//tr")
    
    #len == 1 vì driver lấy header
    assert len(results) == 1

#test bộ lọc số lượng
def testcase_5_filter_by_num(driver):
    testcase_3(driver)

    #default là 10 nhưng lúc load thì sẽ hiển thị toàn bộ
    for i in range (1, 4):
        driver.find_element(By.XPATH, "//body").send_keys(Keys.HOME)

        num_filter = get_clickable_element(driver, By.XPATH, "//div//select[@name='num']")
        num_filter.click()
        num_filter.send_keys(Keys.DOWN)
        num_filter = get_clickable_element(driver, By.XPATH, "//div//select[@name='num']")
        num_filter.send_keys(Keys.ENTER)
        time.sleep(1)
        select_box = driver.find_element(By.NAME, "num")
        select = Select(select_box)
        # Lấy giá trị của option đang được chọn (value)
        selected_option = select.first_selected_option  # Lấy option đang được chọn
        selected_value = selected_option.get_attribute('value')  # Lấy giá trị 'value'
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Cuộn xuống dưới cùng của trang
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Đợi một chút để trang tải thêm phần tử (có thể điều chỉnh thời gian này)
            time.sleep(2)

            # Kiểm tra chiều cao của trang web sau khi cuộn
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            # Nếu không thay đổi chiều cao, có nghĩa là đã tải xong tất cả phần tử
            if new_height == last_height:
                break
            last_height = new_height
        
        results = driver.find_elements(By.XPATH, "//table/tbody//tr")
        #Vì khi chọn hiển thị thì option sẽ tự động cập nhật thành 10 user nên sẽ có điều kiện này
        #check len>31 vì set up db có nhiều hơn 31 user
        if int(selected_value) == 10:
            assert len(results) > 31
        else:
            assert len(results) == int(selected_value)+1

#test bộ lọc trạng thái
def testcase_5_status_filter(driver):
    testcase_3(driver)
    status = {
        "0" : "Chưa được duyệt",
        "1" : "Đã được duyệt",
        "-1": "Đã từ chối",
        "2": "Tài khoản đã bị khoá"
    }
    #tính số lượng các option để loop
    options = driver.find_elements(By.XPATH, "//select[@name='status']//option")
    for i in range (0, len(options)):
        time.sleep(1)
        driver.find_element(By.XPATH, "//body").send_keys(Keys.HOME)

        #Chọn filter
        status_filter = get_clickable_element(driver, By.XPATH, "//div//select[@name='status']")
        status_filter.click()
        status_filter.send_keys(Keys.DOWN)
        status_filter = get_clickable_element(driver, By.XPATH, "//div//select[@name='status']")
        status_filter.send_keys(Keys.ENTER)
        time.sleep(1)
        #Lấy giá trị option
        select_box = driver.find_element(By.NAME, "status")
        select = Select(select_box)
        # Lấy giá trị của option đang được chọn (value)
        selected_option = select.first_selected_option  # Lấy option đang được chọn
        selected_value = selected_option.get_attribute('value')
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Cuộn xuống dưới cùng của trang
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Đợi một chút để trang tải thêm phần tử (có thể điều chỉnh thời gian này)
            time.sleep(2)

            # Kiểm tra chiều cao của trang web sau khi cuộn
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            # Nếu không thay đổi chiều cao, có nghĩa là đã tải xong tất cả phần tử
            if new_height == last_height:
                break
            last_height = new_height
        
        #Lấy thông tin user
        results = driver.find_elements(By.XPATH, "//table/tbody//tr//td[3]")
        #Kiểm tra từng user
        for i in range(1, len(results)):
            assert status[selected_value].lower() in str(results[i].text).lower()

#test bộ lọc phân loại người dùng
#Fail vì lọc không hoạt động
def testcase_5_user_type_filter(driver):
    testcase_3(driver)
    #tính số lượng các option để loop
    options = driver.find_elements(By.XPATH, "//select[@name='role']//option")
    for i in range (0, len(options)):
        time.sleep(1)
        driver.find_element(By.XPATH, "//body").send_keys(Keys.HOME)

        #Chọn filter
        type_filter = get_clickable_element(driver, By.XPATH, "//div//select[@name='role']")
        type_filter.click()
        type_filter.send_keys(Keys.DOWN)
        type_filter = get_clickable_element(driver, By.XPATH, "//div//select[@name='role']")
        type_filter.send_keys(Keys.ENTER)
        time.sleep(1)
        #Lấy giá trị option
        select_box = driver.find_element(By.NAME, "role")
        select = Select(select_box)
        # Lấy giá trị của option đang được chọn (value)
        selected_option = select.first_selected_option  # Lấy option đang được chọn
        selected_value = selected_option.text
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Cuộn xuống dưới cùng của trang
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Đợi một chút để trang tải thêm phần tử (có thể điều chỉnh thời gian này)
            time.sleep(2)

            # Kiểm tra chiều cao của trang web sau khi cuộn
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            # Nếu không thay đổi chiều cao, có nghĩa là đã tải xong tất cả phần tử
            if new_height == last_height:
                break
            last_height = new_height
        
        #Lấy thông tin user
        
        results = driver.find_elements(By.XPATH, "//table/tbody//tr//td[4]")
        #Kiểm tra từng user
        for i in range(1, len(results)):
            assert selected_value.lower() in str(results[i].text).lower()

#Test áp dụng nhiều bộ lọc
def testcase_5_user_type_filter(driver):
    testcase_3(driver)
    #Chọn filter
    num_filter = get_clickable_element(driver, By.XPATH, "//div//select[@name='num']")
    num_filter.click()
    num_filter.send_keys(Keys.DOWN)
    num_filter.send_keys(Keys.ENTER)

    status_filter = get_clickable_element(driver, By.XPATH, "//div//select[@name='status']")
    status_filter.click()
    status_filter.send_keys(Keys.DOWN)
    status_filter.send_keys(Keys.ENTER)
    time.sleep(1)
    
    #vì chỉ check 1 lần nên không cần lấy value
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Cuộn xuống dưới cùng của trang
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Đợi một chút để trang tải thêm phần tử (có thể điều chỉnh thời gian này)
        time.sleep(2)

        # Kiểm tra chiều cao của trang web sau khi cuộn
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Nếu không thay đổi chiều cao, có nghĩa là đã tải xong tất cả phần tử
        if new_height == last_height:
            break
        last_height = new_height
    
    #Lấy thông tin user
    num_results = driver.find_elements(By.XPATH, "//table/tbody//tr")
    status_results = driver.find_elements(By.XPATH, "//table/tbody//tr//td[3]")
    #Kiểm tra từng user
    assert len(num_results) == 21
    for i in range(1, len(status_results)):
        assert "Chưa được duyệt".lower() in str(status_results[i].text).lower()  

#Test add nhiều tài khoản bằng admin
def test_add_multi_user(driver):
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

    for i in range(0, 30):
        #Đăng nhập admin
        driver.find_element(By.NAME, "email").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("123")
        login_button = get_clickable_element(driver, By.XPATH, "//form//button")
        login_button.click()    
        #Điều hướng sang quản lý user
        user_nav = get_clickable_element(driver, By.XPATH, "//div[@class='nav-space']/p[text()='Quản lý tài khoản']")
        user_nav.click()
        time.sleep(0.5)
        #Chọn nút thêm user
        add_new_user = get_clickable_element(driver, By.ID, "new-user")
        add_new_user.click()
        time.sleep(0.5)
        #Điền thông tin
        random_sdt = randint(111111, 999999)
        random_cccd = randint(100000, 999999)
        driver.find_element(By.NAME, "email").send_keys(f"user{i}@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("lmt123")
        driver.find_element(By.NAME, "name").send_keys(f"User {i}")
        driver.find_element(By.NAME, "number").send_keys(f"0{random_sdt+i}")
        driver.find_element(By.NAME, "cccd").send_keys(f"083{random_cccd+i}")
        driver.find_element(By.NAME, "address").send_keys("lVieejt Nam")

        sex_btn = get_clickable_element(driver, By.XPATH, "//input[@name='gender']")
        sex_btn.click()
        driver.find_element(By.XPATH, "//input[@type='date']").send_keys("06232003")
        driver.find_element(By.XPATH, "//body").send_keys(Keys.PAGE_DOWN)

        submit_btn = get_clickable_element(driver, By.XPATH, "//button[text()='Tạo Tài Khoản']")
        submit_btn.click()
        time.sleep(5)
        message = driver.find_element(By.XPATH, "//div[@class='container']/form/a").text
        assert "Tạo tài khoản thành công, vui vòng đăng nhập" in message


#Test chức năng xem chi tiết tài khoản user
def testcase_6(driver, keyword=None):
    #modify phần này để sử dụng lại việc check thông tin user sau khi thay đổi thông tin
    if keyword:
        testcase_4_valid_email_input(driver, keyword)
    else:
        testcase_3(driver)

    #Lấy thông tin của người dùng thứ index+1, vd: người dùng 1 thì index = 1+1
    index = 2
    user_info = driver.find_elements(By.XPATH, f"//table/tbody//tr[{index}]//td")
    #lưu thông tin vào 1 dict
    dict_user_info = {
        "Email": str(user_info[0].text).lower(),
        "name": str(user_info[1].text).lower(),
        "Status": str(user_info[2].text).lower(),
        "create_day": str(user_info[4].text).lower()
    }
    
    #Chọn nút chi tiết
    user_detail_btn = get_clickable_element(driver, By.XPATH, f"//table/tbody//tr[{index}]//td[6]//form//button")
    user_detail_btn.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//body").send_keys(Keys.END)
    time.sleep(1)
    user_email = driver.find_element(By.XPATH, "//div[@class='form']/div/h3").text
    user_name = driver.find_element(By.NAME, "ten").get_attribute('value')
    user_status = driver.find_element(By.XPATH, "//select[@name='status']").text
    
    #default role khi tải trang luôn là sinh viên nên không check nữa
    # user_role = driver.find_element(By.NAME, "rank")
    # select = Select(user_role)
    # # Lấy giá trị của option đang được chọn (value)
    # selected_option = select.first_selected_option  # Lấy option đang được chọn
    # selected_value = selected_option.text
    
    user_create_day = driver.find_element(By.XPATH, "//div[@class='form']/div/p").text

    assert dict_user_info['Email'] in user_email
    assert dict_user_info['name'] in user_name
    assert dict_user_info['Status'] in str(user_status).lower()
    assert dict_user_info['create_day'] in user_create_day

#Test chức năng thay đổi thông tin tài khoản
#Fail vì chức năng cập nhật sai
def testcase_7(driver):
    #tìm kiếm user bằng email
    email = "lmt@gmail.com"
    testcase_4_valid_email_input(driver, email)

    #chọn nút xem chi tiết
    user_detail_btn = get_clickable_element(driver, By.XPATH, "//table/tbody//tr[2]//td[6]//form//button")
    user_detail_btn.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//body").send_keys(Keys.END)
    time.sleep(1)

    new_name = "RanDom Tri"
    new_role = "Công chức"

    #Đổi thành tên mới
    user_name = driver.find_element(By.NAME, "ten")
    user_name.clear()
    user_name.send_keys(new_name)
    
    #đổi role mới
    user_role = driver.find_element(By.NAME, "rank")
    select = Select(user_role)
    # Lấy giá trị của option đang được chọn (value)
    select.select_by_visible_text(new_role)
    
    tac = get_clickable_element(driver, By.NAME, "tac")
    tac.click()

    save_btn = get_clickable_element(driver, By.XPATH, "//div[@class='buttons']//button[1]")
    save_btn.click()

    testcase_4_valid_email_input(driver, email)

    user_info = driver.find_elements(By.XPATH, f"//table/tbody//tr[2]//td")

    assert new_name == user_info[1].text
    assert new_role.lower() == str(user_info[3].text).lower()
