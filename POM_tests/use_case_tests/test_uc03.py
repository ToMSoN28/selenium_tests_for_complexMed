import pytest
import random
from pages.patient_page import PatientPage
from pages.search_patient_page import SearchPatientPage

class TestUC03: # Wyszukanie pacjenta
    
    users = ['manager', 'doctor', 'receptionist']
    
    def login_and_go_to_search_patient(self, login, setup_method, user_credentials, user):
        user_l, user_p = user_credentials[user]
        login(user_l, user_p)
        driver, base_url = setup_method
        search_patient_page = SearchPatientPage(driver, base_url)
        search_patient_page.click_on_search_patient()
        return search_patient_page
    
    @pytest.mark.parametrize("first_name, last_name, phone", [
        ("", "", ""),
        ("ar", "", ""),
        ("", "ski", ""),
        ("", "", "1"),
        ("na", "sk", ""),
        ("a", "", "700"),
        ("", "ń", "5"),
        ("x", "y", "0")
    ])
    def test_search_patient(self, login, setup_method, user_credentials, patient_list, first_name, last_name, phone):
        user = random.choice(self.users)
        search_patient_page = self.login_and_go_to_search_patient(login, setup_method, user_credentials, user)
        search_patient_page.enter_first_name_in_patient_sherch(first_name)
        search_patient_page.enter_last_name_in_patient_sherch(last_name)
        search_patient_page.enter_phone_in_patient_sherch(phone)
        search_patient_page.click_on_search_button()
        patients_list = search_patient_page.get_patient_list()
        patients_list = [sublist[1:] for sublist in patients_list]
        expected_table = []
        for patient in patient_list:
            if first_name in patient['first_name'] and last_name in patient['last_name'] and phone in patient['phone']:
                full_name = f'{patient['first_name']} {patient['last_name']}'
                expected_table.append([full_name, patient['birth_date'], patient['pesel'], patient['phone']])
        assert patients_list == expected_table