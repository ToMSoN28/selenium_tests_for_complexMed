import pytest
import time, random
from dateutil import parser
from typing import Tuple
from datetime import datetime
from pages.patient_page import PatientPage
from pages.search_patient_page import SearchPatientPage

class TestUC05: #Sprawdzenie przyszłych wizyt pacjenta
    
    def login_and_go_to_patien_page_by_patient_number(self, login, setup_method, user_credentials, patient_list, patient_number: int, user: str) -> PatientPage:
        user_l, user_p = user_credentials[user]
        login(user_l, user_p)
        driver, base_url = setup_method
        search_patient_page = SearchPatientPage(driver, base_url)
        search_patient_page.click_on_search_patient()
        time.sleep(0.5)
        search_patient_page.click_on_search_button()
        patient_info_list = search_patient_page.get_patient_list()
        patient_id = None
        for patient in patient_info_list:
            if patient[3] == patient_list[patient_number]['pesel']:
                patient_id = patient[0]
        search_patient_page.click_on_patient_profile(patient_id)
        patient_page = PatientPage(driver, base_url)
        return patient_page
    
    def create_time_interval(self, date_str: str, time_range: str) -> Tuple[datetime, datetime]:
        date_str = date_str.replace('.', '').strip()
        date = parser.parse(date_str)
        print(f'prase date: {date}')
        start_time_str, end_time_str = time_range.split(' - ')
        start_datetime = datetime.combine(date.date(), datetime.strptime(start_time_str.strip(), '%H:%M').time())
        end_datetime = datetime.combine(date.date(), datetime.strptime(end_time_str.strip(), '%H:%M').time())
        return start_datetime, end_datetime
    
    @pytest.mark.parametrize("user", [
        ("manager"),
        ("doctor"),
        ("receptionist")
    ])
    def test_visible_upcoming_visits(self, login, setup_method, user_credentials, patient_list, user):
        patient_number = random.randint(0,9)
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, patient_number, user)
        assert patient_page.visible_check_upcoming_visits()  
    
    @pytest.mark.parametrize("user", [
        ("manager"),
        ("doctor"),
        ("receptionist")
    ])    
    def test_upcoming_visit_information(self, login, setup_method, user_credentials, patient_list, user):
        patient_number = random.randint(0,9)
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, patient_number, user)
        today = datetime.today()
        upcoming = patient_page.get_upcoming_visits()
        print(upcoming)
        upcoming_datatime = []
        for v in upcoming:
            upcoming_datatime.append(self.create_time_interval(v[2], v[3]))
        for i in range(len(upcoming)-1):
            assert upcoming_datatime[i][0] < upcoming_datatime[i+1][0]
            assert today < upcoming_datatime[i][0]
    
    @pytest.mark.parametrize("user", [
        ("manager"),
        ("doctor"),
        ("receptionist")
    ])        
    def test_redirection_after_click_on_detal_in_upcoming_visit(self, login, setup_method, user_credentials, patient_list, get_current_url, user):
        patient_number = random.randint(0,9)
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, patient_number, user)
        upcoming = patient_page.get_upcoming_visits()
        # upcoming_visit = random.choice(upcoming)
        for upcoming_visit in upcoming:
            patient_page.click_on_detail_in_upcoming_visit(upcoming_visit[0])
            upcoming_num = upcoming_visit[0].replace("visit",'')
            assert f'/visit/{upcoming_num}/' == get_current_url(patient_page.driver)  
            patient_page.driver.back()