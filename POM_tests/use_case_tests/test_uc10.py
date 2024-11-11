import pytest
import time, random
from pages.visit_page import VisitPage
from pages.patient_page import PatientPage
from pages.search_patient_page import SearchPatientPage

class TestUC10:
    
    def login_fun(self, login, setup_method, user_credentials, user: str) -> VisitPage:
        user_l, user_p = user_credentials[user]
        login(user_l, user_p)
        driver, base_url = setup_method
        visit_page = VisitPage(driver, base_url)
        return visit_page
    
    def go_to_patient_profile(self, driver, patient_list, patient_number) -> None:
        search_patient_page = SearchPatientPage(driver, None)
        search_patient_page.click_on_search_patient()
        time.sleep(0.5)
        search_patient_page.click_on_search_button()
        patient_info_list = search_patient_page.get_patient_list()
        patient_id = None
        for patient in patient_info_list:
            if patient[3] == patient_list[patient_number]['pesel']:
                patient_id = patient[0]
        search_patient_page.click_on_patient_profile(patient_id)
        
    def go_to_past_visit(self, driver, past_num) -> int:
        patient_page = PatientPage(driver, None)
        past = patient_page.get_past_visits()
        past_visit = past[past_num]
        patient_page.click_on_detail_in_past_visit(past_visit[0])
        return len(past) 
    
    def go_to_upcoming_visit(self, driver, past_num) -> int:
        patient_page = PatientPage(driver, None)
        upcoming = patient_page.get_upcoming_visits()
        upcoming_visit = upcoming[past_num]
        patient_page.click_on_detail_in_upcoming_visit(upcoming_visit[0])
        return len(upcoming) 
    
    @pytest.mark.parametrize("user, visible", [
        ("receptionist", False),
        ("manager", False),
        ("doctor", True) 
    ])
    def test_visible_desc_of_visits(self, login, setup_method, user_credentials, patient_list, user, visible):
        patient_number = random.randint(0,9)
        visit_page = self.login_fun(login, setup_method, user_credentials, user)
        self.go_to_patient_profile(visit_page.driver, patient_list, patient_number)
        patient_page = PatientPage(visit_page.driver, visit_page.base_url)
        if patient_page.visible_check_past_visits():
            past = patient_page.get_past_visits()
            for past_id in past:
                patient_page.click_on_detail_in_past_visit(past_id[0])
                time.sleep(0.5)
                assert visit_page.visible_check_visit_description() == visible
                visit_page.driver.back()
        if patient_page.visible_check_upcoming_visits():
            upcoming = patient_page.get_upcoming_visits()
            for upcoming_id in upcoming:
                patient_page.click_on_detail_in_upcoming_visit(upcoming_id[0])
                time.sleep(0.5)
                assert visit_page.visible_check_visit_description() == visible
                visit_page.driver.back()

    
    