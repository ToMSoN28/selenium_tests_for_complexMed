import time
from pages.patient_registration_page import PatientRegistrationPage


class TestPatientRegistrationPage:
    
    recepcionist = ("receptionist1", "pass1234")
        
    # wyniesienie i parametryzacje do wypełnienia formularza
        
    def test_adding_patient_with_pesel_that_already_exist_in_system(self, login, setup_method):
        login(self.recepcionist[0], self.recepcionist[1])
        driver, base_url = setup_method
        patient_registration_page = PatientRegistrationPage(driver, base_url)
        patient_registration_page.click_on_patient_registration()
        patient_registration_page.enter_patient_first_name('Mark')
        patient_registration_page.enter_patient_last_name('Kuban')
        patient_registration_page.enter_patient_pesel('04261771994')
        patient_registration_page.enter_patient_phone_number('123234345')
        patient_registration_page.click_on_register_button()
        time.sleep(1)
        assert f'Patient with pesel {'04261771994'} already exist' == patient_registration_page.check_error_message()