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
        time.sleep(3.5)
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
        "doctor_with_wrong_password": ("doctor1", "1234pass"),
        "random": ("Xyz", "qwerty12")
    }
    
@pytest.fixture(scope="session")
def patient_list():
    return [
        {"first_name": "Anna", "last_name": "Nowak", "birth_date": "October 10, 2002", "pesel": "02301037664", "phone": "600700801"},
        {"first_name": "Ewa", "last_name": "Zielińska", "birth_date": "August 1, 1980", "pesel": "80080144423", "phone": "600700805"},
        {"first_name": "Jan", "last_name": "Kowalski", "birth_date": "June 17, 2004", "pesel": "04261771994", "phone": "600700800"},
        {"first_name": "Joanna", "last_name": "Jankowska", "birth_date": "May 12, 1953", "pesel": "53051268628", "phone": "600700809"},
        {"first_name": "Katarzyna", "last_name": "Wójcik", "birth_date": "January 15, 1994", "pesel": "94111582546", "phone": "600700803"},
        {"first_name": "Magdalena", "last_name": "Woźniak", "birth_date": "July 7, 1971", "pesel": "71070704260", "phone": "600700807"},
        {"first_name": "Marek", "last_name": "Kowalczyk", "birth_date": "July 30, 1992", "pesel": "92073093870", "phone": "600700804"},
        {"first_name": "Paweł", "last_name": "Kozłowski", "birth_date": "February 15, 1957", "pesel": "57021597837", "phone": "600700808"},
        {"first_name": "Piotr", "last_name": "Wiśniewski", "birth_date": "July 16, 1997", "pesel": "97071654694", "phone": "600700802"},
        {"first_name": "Tomasz", "last_name": "Szymański", "birth_date": "January 6, 1979", "pesel": "79110688653", "phone": "600700806"}
    ]
    
@pytest.fixture(scope="session")
def visit_name_list():
    return [
        "Konsultacja ortopedyczna",
        "Leczenie urazów",
        "Masaż leczniczy pleców",
        "Diagnostyka bólu stawów",
        "Kontrola po operacji",
        "Badanie USG",
        "Iniekcje dostawowe",
        "Diagnostyka złamań",
        "Ocena postawy ciała",
        "Rehabilitacja"
    ]
    
@pytest.fixture(scope="session")
def doctors_list():
    return [
        "Adam Wiśniewski",
        "Ewa Szymańska"
    ]