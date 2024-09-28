import pytest
from typing import List
from pages.search_patient_page import SearchPatientPage


class TestSearchPatientPage:
    
    patients_info = [
        {"first_name": "Anna", "last_name": "Nowak", "birth_date": "October 10, 2002", "pesel": "02301037664", "phone": "600700801"},
        {"first_name": "Ewa", "last_name": "Zielińska", "birth_date": "August 1, 1980", "pesel": "80080144423", "phone": "600700805"},
        {"first_name": "Jan", "last_name": "Kowalski", "birth_date": "June 17, 2004", "pesel": "04261771994", "phone": "600700800"},
        {"first_name": "Joanna", "last_name": "Jankowska", "birth_date": "May 12, 1953", "pesel": "53051268628", "phone": "600700809"},
        {"first_name": "Katarzyna", "last_name": "Wójcik", "birth_date": "January 15, 1994", "pesel": "94111582546", "phone": "600700803"},
        {"first_name": "Magdalena", "last_name": "Woźniak", "birth_date": "July 7, 1971", "pesel": "71070704260", "phone": "600700807"},
        {"first_name": "Marek", "last_name": "Kowalczyk", "birth_date": "July 30, 1992", "pesel": "92073093870", "phone": "600700804"},
        {"first_name": "Paweł", "last_name": "Kozłowski", "birth_date": "February 15, 1957", "pesel": "57021597837", "phone": "600700808"},
        {"first_name": "Piotr", "last_name": "Wiśniewski", "birth_date": "July 16, 1997", "pesel": "97071654694", "phone": "600700802"},
        {"first_name": "Tomasz", "last_name": "Szymański", "birth_date": "January 6, 1979", "pesel": "79110688653", "phone": "600700806"}
    ]
    
    def convert_patient_into_list(self, list: List[int]) -> List[List]:
        result = []
        for i, patient in enumerate(self.patients_info):
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
    def test_search_patient(self, login, setup_method, user_credentials, first_name, last_name, phone):
        search_patient_page = self.login_and_go_to_search_patient(login, setup_method, user_credentials)
        search_patient_page.enter_first_name_in_patient_sherch(first_name)
        search_patient_page.enter_last_name_in_patient_sherch(last_name)
        search_patient_page.enter_phone_in_patient_sherch(phone)
        search_patient_page.click_on_search_button()
        patients_list = search_patient_page.get_patient_list()
        expected_table = []
        for patient in self.patients_info:
            if first_name in patient['first_name'] and last_name in patient['last_name'] and phone in patient['phone']:
                full_name = f'{patient['first_name']} {patient['last_name']}'
                expected_table.append([full_name, patient['birth_date'], patient['pesel'], patient['phone']])
        assert patients_list == expected_table
        