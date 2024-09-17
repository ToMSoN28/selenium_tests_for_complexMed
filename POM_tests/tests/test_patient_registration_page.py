import time
from pages.patient_registration_page import PatientRegistrationPage


class TestPatientRegistrationPage:
    
    def fill_and_send_adding_patirnt_form(self, login, setup_method, user_credentials, user: str, first_name: str, last_name: str, pesel: str, phone_number: str) -> PatientRegistrationPage:
        user_l, user_p = user_credentials[user]
        login(user_l, user_p)
        driver, base_url = setup_method
        patient_registration_page = PatientRegistrationPage(driver, base_url)
        patient_registration_page.click_on_patient_registration()
        patient_registration_page.enter_patient_first_name(first_name)
        patient_registration_page.enter_patient_last_name(last_name)
        patient_registration_page.enter_patient_pesel(pesel)
        patient_registration_page.enter_patient_phone_number(phone_number)
        patient_registration_page.click_on_register_button()
        time.sleep(1) 
        return patient_registration_page
        
    def test_adding_patient_with_pesel_that_already_exist_in_system(self, login, setup_method, user_credentials):
        user = 'receptionist'
        patient_registration_page = self.fill_and_send_adding_patirnt_form(login, setup_method, user_credentials, user, 'Mark', 'Kuban', '04261771994', '123234345')
        
        assert f'Patient with pesel {'04261771994'} already exist' == patient_registration_page.check_error_message()