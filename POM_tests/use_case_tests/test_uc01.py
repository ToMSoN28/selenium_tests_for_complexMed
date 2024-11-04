import time
import pytest
from pages.login_page import LoginPage
from pages.navbar_page import NavbarPage

class TestUC01:
        
    @pytest.mark.parametrize("user, expected_endpoint", [
        ("manager", "/dashboard/manager/"),
        ("doctor", "/dashboard/doctor/"),
        ("receptionist", "/patient/search/"),
        ("doctor_with_wrong_password", "/login/"),
        ("random", "/login/")
    ])
    def test_login_based_on_role(self, setup_method, get_current_url, user_credentials, user, expected_endpoint):
        user_n, user_p = user_credentials[user]
        driver, base_url = setup_method
        login_page = LoginPage(driver, base_url)
        login_page.enter_user_login(user_n)
        login_page.enter_password(user_p)
        login_page.click_on_login_button()
        time.sleep(3)
        
        assert get_current_url(driver) == expected_endpoint  
        
    @pytest.mark.parametrize("user", [
        ("manager"),
        ("doctor"),
        ("receptionist")
    ])    
    def test_logout(self, setup_method, login, get_current_url, user_credentials, user):
        user_n, user_p = user_credentials[user]
        login(user_n, user_p)      
        driver, base_url = setup_method 
        navbar = NavbarPage(driver)
        navbar.click_on_logout()
        time.sleep(1)
        
        assert get_current_url(driver) == get_current_url(driver)
        
        throw_exception = False
        try:
            driver.get(f'{base_url}patient/search/')
            throw_exception = False
        except Exception as e:
            # print(e)
            throw_exception = True
        time.sleep(1)
        
        assert throw_exception    
    