from urllib.parse import urlparse
import pytest
import time
from selenium import webdriver
from pages.login_page import LoginPage
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope='function')
def setup_method():
    # Przed każdym testem
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    base_url = 'http://127.0.0.1:8000/'
    login_page = LoginPage(driver=driver, base_url=base_url)
    login_page.open_login_page()
    yield driver, login_page
    # Po każdym teście
    driver.get(f'{base_url}logout/')
    driver.quit()

@pytest.fixture
def login(setup_method):
    def _login(user_login, password):
        driver, login_page = setup_method
        login_page.enter_user_login(user_login)
        login_page.enter_password(password)
        login_page.click_on_login_button()
        time.sleep(3)
    return _login

@pytest.fixture
def logout(setup_method):
    def _logout():
        driver, base_url = setup_method
        driver.get(f'{base_url}logout/')

@pytest.fixture
def get_current_url():
    def _get_current_url(driver):
        return urlparse(driver.current_url).path
    return _get_current_url

@pytest.fixture(scope="session")
def user_credentials():
    return {
        "receptionist": ("receptionist1", "pass1234"),
        "manager": ("manager1", "pass1234"),
        "doctor": ("doctor1", "pass1234"),
        "random": ("Xyz", "qwerty12")
    }