import time
import pytest
from typing import List
from pages.patient_page import PatientPage
from pages.search_patient_page import SearchPatientPage


class TestPatientPage:
    
    weeks = [
        'This week',
        'Next week',
        'In two weeks'
    ]
    
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
        
    def test_choose_doctor_in_search_visit_module(self, login, setup_method, user_credentials, patient_list, doctors_list):
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, 0)
        doctors = patient_page.get_available_doctors()
        for doctor in doctors[1:]:
            assert doctor.text in doctors_list
            
    def test_choose_weeks_in_search_visit_module(self, login, setup_method, user_credentials, patient_list):
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, 0)
        weeks = patient_page.get_available_weeks()
        for week in weeks[1:]:
            assert week.text in self.weeks
            
    def test_visible_days_navigation_segment_in_available_visits(self, login, setup_method, user_credentials, patient_list):
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, 0)
        assert not patient_page.visible_check_days_navigation_segment()
        patient_page.select_week_by_visible_text(self.weeks[2])
        patient_page.click_on_search_button()
        assert patient_page.visible_check_days_navigation_segment()
        
    def test_days_navigation_segment_in_available_visits(self, login, setup_method, user_credentials, patient_list):
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, 5)
        patient_page.select_week_by_visible_text(self.weeks[2])
        patient_page.click_on_search_button()
        time.sleep(5)
        days = patient_page.get_visible_days_from_days_nav_segment()
        print(days)
        for i, day in enumerate(days):
            assert day == f'link-{i+1}'
            patient_page.click_on_day_from_days_nav_segment(day)
            time.sleep(1.5)
            assert patient_page.visible_check_dayli_visits_section(day)
            
    # pobranie danych o przefiltrowanych wizytach czy lekarzach i tygodniach rózne kombinacje (patrzeć czy jest widoczne wyniki jak test w piątek)
            
        