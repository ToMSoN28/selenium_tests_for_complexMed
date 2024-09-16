import time
import pytest
from pages.login_page import LoginPage

class TestLoginPage:
        
    @pytest.mark.parametrize("user, expected_endpoint", [
        ("manager", "/dashboard/manager/"),
        ("doctor", "/dashboard/doctor/"),
        ("receptionist", "/patient/search/"),
        ("random", "/login/")
    ])
    def test_role_based_login(self, setup_method, get_current_url, user_credentials, user, expected_endpoint):
        user_n, user_p = user_credentials[user]
        driver, base_url = setup_method
        login_page = LoginPage(driver, base_url)
        login_page.enter_user_login(user_n)
        login_page.enter_password(user_p)
        login_page.click_on_login_button()
        time.sleep(3)
        
        assert get_current_url(driver) == expected_endpoint        
    