import pytest
from typing import List
from pages.patient_page import PatientPage
from pages.search_patient_page import SearchPatientPage


class TestPatientPage:
    
    def login_and_go_to_patien_page_by_patient_number(self, login, setup_method, user_credentials, patient_list, patient_number: int) -> PatientPage:
        user = 'receptionist'
        user_l, user_p = user_credentials[user]
        login(user_l, user_p)
        driver, base_url = setup_method
        search_patient_page = SearchPatientPage(driver, base_url)
        search_patient_page.click_on_search_button()
        patient_info_list = search_patient_page.get_patient_list()
        patient_id = None
        for patient in patient_info_list:
            if patient[3] == patient_list[patient_number]['pesel']:
                patient_id = patient[0]
        search_patient_page.click_on_patient_profile(patient_id)
        patient_page = PatientPage(driver, base_url)
        return patient_page
    
    def test_visible_search_visit_module(self, login, setup_method, user_credentials, patient_list):
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, 0)
        assert patient_page.visible_check_search_available_visit_panel()
        
    def test_choose_visit_name_in_search_visit_module(self, login, setup_method, user_credentials, patient_list, visit_name_list):
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, 0)
        visit_name_options = patient_page.get_available_visit_names()
        for visit_name in visit_name_options[1:]:
            assert visit_name.text in visit_name_list
        
        # for patient in patient
        