import time

import pytest
from pages.change_password_page import ChangePasswordPage


class TestChangePasswordPage:
    
    def fill_and_send_change_password_form(self, login, setup_method, user_credentials, user: str, old_password: str, new_password: str, confirm_password: str, use_user_passwort = False) -> ChangePasswordPage:
        user_l, user_p = user_credentials[user]
        if use_user_passwort:
            login(user_l, user_p)
        else:
            login(user_l, old_password)
        driver, base_url = setup_method
        change_password_page = ChangePasswordPage(driver, base_url)
        change_password_page.click_on_new_password()
        change_password_page.enter_old_password(old_password)
        change_password_page.enter_new_password(new_password)
        change_password_page.enter_confirm_password(confirm_password)
        change_password_page.click_on_change_button()
        time.sleep(5)
        return change_password_page
    
    def test_changing_password_with_wrong_old_password(self, login, setup_method, user_credentials ):
        user = 'doctor'
        _, wrong_password = user_credentials['doctor_with_wrong_password']
        new_password = 'p1a2s3s4'
        change_password_page = self.fill_and_send_change_password_form(login, setup_method, user_credentials, user, wrong_password, new_password, new_password, use_user_passwort=True)
        
        assert 'Incorrect old password! Try again.' == change_password_page.check_error_message()
        
    def test_changing_password_with_wrong_confirmation_password(self, login, setup_method, user_credentials ):
        user = 'doctor'
        new_password = '1234pass'
        wrong_confirmation_password = '1234pa'
        _, old_password = user_credentials[user]
        change_password_page = self.fill_and_send_change_password_form(login, setup_method, user_credentials, user, old_password, new_password, wrong_confirmation_password)
    
        assert 'New passwords are not the same! Try again.' == change_password_page.check_error_message()
    
    @pytest.mark.parametrize("user, expected_endpoint", [
        ("manager", "/dashboard/manager/"),
        ("doctor", "/dashboard/doctor/"),
        ("receptionist", "/patient/search/")
    ])    
    def test_corect_changing_password(self, login, setup_method, user_credentials, get_current_url, user, expected_endpoint ):
        new_password = '1234pass'
        _, old_password = user_credentials[user]
        driver, _ = setup_method
        change_password_page = self.fill_and_send_change_password_form(login, setup_method, user_credentials, user, old_password, new_password, new_password)
        
        assert expected_endpoint == get_current_url(driver)
        change_password_page.click_on_logout()
        change_password_page = self.fill_and_send_change_password_form(login, setup_method, user_credentials, user, new_password, old_password, old_password)
        
        assert expected_endpoint == get_current_url(driver)
