import pytest
from pages.navbar_page import NavbarPage


class TestNavbarPage:
        
    @pytest.mark.parametrize("user, expected_result", [
        ("manager", [False, True, True, True, True, True, True]),
        ("doctor", [True, False, True, False, False, False, True]),
        ("receptionist", [False, True, True, False, False, False, True])
    ])    
    def test_visible_navatribute_for_erery_role(self, login, setup_method, user_credentials, user, expected_result):
        print(user_credentials[user])
        user_n, user_p = user_credentials[user]
        login(user_n, user_p)
        driver, _ = setup_method
        result = []
        navbar_page = NavbarPage(driver)
        result.append(navbar_page.visible_check_daily_visits())
        result.append(navbar_page.visible_check_patient_registration())
        result.append(navbar_page.visible_check_search_patient())
        result.append(navbar_page.visible_check_edit_schedule())
        result.append(navbar_page.visible_check_worker_list())
        result.append(navbar_page.visible_check_create_account())
        result.append(navbar_page.visible_check_person_menu_button())
        
        assert result == expected_result
        
    @pytest.mark.parametrize("user_login, password", [
        ("manager1", "pass1234")
    ])
    def test_click_on_navatribute__workers_list__new_password__edit_schedule(self, login, setup_method, get_current_url, user_login, password):
        login(user_login, password)
        driver, _ = setup_method
        navbar_page = NavbarPage(driver)
        
        navbar_page.click_on_worker_list()   
        assert get_current_url(driver) == '/workers-list/'
        
        navbar_page.click_on_person_menu_button()
        navbar_page.click_on_new_password()
        assert get_current_url(driver) == '/change-password/'
        
        navbar_page.click_on_edit_schedule()
        assert get_current_url(driver) == '/dashboard/manager/'
        
    @pytest.mark.parametrize("user_login, password", [
        ("doctor1", "pass1234")
    ])
    def test_click_on_navatribute__search_patient__daily_visit(self, login, setup_method, get_current_url, user_login, password):
        login(user_login, password)
        driver, _ = setup_method
        navbar_page = NavbarPage(driver)
        
        navbar_page.click_on_search_patient()
        assert get_current_url(driver) == '/patient/search/'
        
        navbar_page.click_on_daily_visits()
        assert get_current_url(driver) == '/dashboard/doctor/'
        
    @pytest.mark.parametrize("user_login, password", [
        ("receptionist1", "pass1234")
    ])
    def test_click_on_navatribute__patient_registration__logout(self, login, setup_method, get_current_url, user_login, password):
        login(user_login, password)
        driver, _ = setup_method
        navbar_page = NavbarPage(driver)
        
        navbar_page.click_on_patient_registration()
        assert get_current_url(driver) == '/patient-registration/'
        
        navbar_page.click_on_person_menu_button()
        navbar_page.click_on_logout()
        assert get_current_url(driver) == '/login/'
        