import pytest
from typing import List
from pages.patient_page import PatientPage
from pages.search_patient_page import SearchPatientPage


class TestSearchPatientPage:
    
    def convert_patient_into_list(self, patient_list, list: List[int]) -> List[List]:
        result = []
        for i, patient in enumerate(patient_list):
            full_name = f'{patient['first_name']} {patient['last_name']}'
            result.append([full_name, patient['birth_date'], patient['pesel'], patient['phone']])
        return result
    
    def login_and_go_to_search_patient(self, login, setup_method, user_credentials):
        user = 'receptionist'
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
        ("", "ń", "2"),
        ("x", "y", "0")
    ])
    def test_search_patient(self, login, setup_method, user_credentials, patient_list, first_name, last_name, phone):
        search_patient_page = self.login_and_go_to_search_patient(login, setup_method, user_credentials)
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
        
    def test_search_and_go_to_patient_page(self, login, setup_method, user_credentials, get_current_url):
        search_patient_page = self.login_and_go_to_search_patient(login, setup_method, user_credentials)
        search_patient_page.click_on_search_button()
        patients_list = search_patient_page.get_patient_list()
        print(patients_list)
        for patient in patients_list:
            patient_id: str = patient[0]
            search_patient_page.click_on_patient_profile(patient_id)
            current_endpoint = get_current_url(search_patient_page.driver)
            assert current_endpoint == f'/patient/{patient_id.replace('patient', '')}/'
            patient_page = PatientPage(search_patient_page.driver, search_patient_page.base_url)
            patient_info = patient_page.get_patient_information()
            assert patient[1:] == patient_info
            search_patient_page.driver.back()
        