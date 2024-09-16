from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

from pages.login_page import LoginPage
from pages.navbar_page import NavbarPage

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

base_url = 'http://127.0.0.1:8000/'

login_page = LoginPage(driver, base_url)
login_page.open_login_page()
login_page.enter_user_login("receptionist1")
login_page.enter_password("pass1234")
login_page.click_on_login_button()
time.sleep(3)

navbar = NavbarPage(driver)
print(navbar.visible_check_create_account())
print(navbar.visible_check_patient_registration())
navbar.logout()

driver.quit()
    
