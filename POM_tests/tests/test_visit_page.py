import time
import pytest
# import random
# from dateutil import parser
# from typing import List, Tuple
from pages.navbar_page import NavbarPage
# from datetime import datetime, timedelta, timezone
from pages.patient_page import PatientPage
from pages.visit_page import VisitPage
from pages.search_patient_page import SearchPatientPage
# EPOCH = datetime.fromtimestamp(0, timezone.utc)

class TestVisitPage:
    
    def login_fun(self, login, setup_method, user_credentials, user: str) -> VisitPage:
        user_l, user_p = user_credentials[user]
        login(user_l, user_p)
        driver, base_url = setup_method
        visit_page = VisitPage(driver, base_url)
        return visit_page
    
    def go_to_past_visit(self, driver, patient_list, patient_number, past_num) -> int:
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
        patient_page = PatientPage(driver, None)
        past = patient_page.get_past_visits()
        past_visit = past[past_num]
        patient_page.click_on_detail_in_past_visit(past_visit[0])
        return len(past)
        
        
    @pytest.mark.parametrize("user, visible", [
        ("receptionist", False),
        ("manager", False),
        ("doctor", True) 
    ])
    def test_visible_desc_of_visits(self, login, setup_method, user_credentials, patient_list, user, visible):
        visit_page = self.login_fun(login, setup_method, user_credentials, user)
        self.go_to_past_visit(visit_page.driver, patient_list, 3, 0)
        assert visit_page.visible_check_visit_description() == visible
        
        