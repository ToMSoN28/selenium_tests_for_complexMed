import pytest
import random
from pages.patient_page import PatientPage
from pages.search_patient_page import SearchPatientPage

class TestUC02:
        
    def login_and_go_to_search_patient(self, login, setup_method, user_credentials, user):
        user_l, user_p = user_credentials[user]
        login(user_l, user_p)
        driver, base_url = setup_method
        search_patient_page = SearchPatientPage(driver, base_url)
        search_patient_page.click_on_search_patient()
        return search_patient_page
    
    @pytest.mark.parametrize("user", [
        ("manager"),
        ("doctor"),
        ("receptionist")
    ])    
    def test_search_for_every_role(self, setup_method, login, patient_list, user_credentials, user):
        search_patient_page = self.login_and_go_to_search_patient(login, setup_method, user_credentials, user)
        search_patient_page.click_on_search_button()
        patients_list = search_patient_page.get_patient_list()
        patients_list = [sublist[1:] for sublist in patients_list]
        expected_table = []
        for patient in patient_list:
            full_name = f'{patient['first_name']} {patient['last_name']}'
            expected_table.append([full_name, patient['birth_date'], patient['pesel'], patient['phone']])
        assert patients_list == expected_table
        
    