import time
import pytest
from pages.patient_registration_page import PatientRegistrationPage


class TestUC12:
    
    def login(self, login, user_credentials, setup_method, user) -> PatientRegistrationPage:
        user_l, user_p = user_credentials[user]
        login(user_l, user_p)
        driver, base_url = setup_method
        patient_registration_page = PatientRegistrationPage(driver, base_url)
        return patient_registration_page
    
    def fill_and_send_adding_patirnt_form(self, patient_registration_page: PatientRegistrationPage, first_name: str, last_name: str, pesel: str, phone_number: str) -> PatientRegistrationPage:
        patient_registration_page.enter_patient_first_name(first_name)
        patient_registration_page.enter_patient_last_name(last_name)
        patient_registration_page.enter_patient_pesel(pesel)
        patient_registration_page.enter_patient_phone_number(phone_number)
        patient_registration_page.click_on_register_button()
        time.sleep(1) 
        return patient_registration_page
    
    @pytest.mark.parametrize("user, visible", [
        ("manager", True),
        ("doctor", False),
        ("receptionist", True)
    ])
    def test_go_to_patient_registration_panel(self, login, setup_method, user_credentials, get_current_url, user, visible):
        patient_registration_page: PatientRegistrationPage = self.login(login, user_credentials, setup_method, user)
        assert patient_registration_page.visible_check_patient_registration() == visible
        if visible:
            patient_registration_page.click_on_patient_registration()
            assert get_current_url(patient_registration_page.driver) == '/patient-registration/'
        
    @pytest.mark.parametrize("user", [
        ("manager"),
        ("receptionist")
    ])     
    def test_adding_patient_with_pesel_that_already_exist_in_system(self, login, setup_method, user_credentials, user):
        patient_registration_page: PatientRegistrationPage = self.login(login, user_credentials, setup_method, user)
        patient_registration_page.click_on_patient_registration()
        self.fill_and_send_adding_patirnt_form(patient_registration_page, 'Mark', 'Kuban', '04261771994', '123234345')
        
        assert f'Patient with pesel {'04261771994'} already exist' == patient_registration_page.check_error_message()
        
    # dodać poprawnie 