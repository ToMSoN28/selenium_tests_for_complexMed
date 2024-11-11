import time
import pytest
import random
from dateutil import parser
from datetime import datetime, timedelta
from pages.visit_page import VisitPage
from pages.patient_page import PatientPage
from pages.search_patient_page import SearchPatientPage


class TestUC14:
    
    def in_witch_week_is_date(self, data_special: str) -> str|None:
        date_str = data_special.split("     ")[0].split(": ")[1]
        time_str = data_special.split("     ")[1].split(" - ")[0]
        datetime_str = f"{date_str} {time_str}"
        target_date = datetime.strptime(datetime_str, "%d %B, %Y %H:%M")
        today = datetime.today()
        current_week = today.isocalendar().week
        target_week = target_date.isocalendar().week
        current_year = today.year
        target_year = target_date.year
        if target_year == current_year:
            if target_week == current_week:
                return 'This week'
            elif target_week == current_week + 1:
                return 'Next week'
            elif target_week == current_week + 2:
                return 'In two weeks'
        return None
    
    def transrofm_info_to_data_special(self, date_str: str, start: str, end: str) -> str:
        date = parser.parse(date_str)
        formatted_string = f"{date.strftime('%A')}: {date.strftime('%d %B, %Y')}     {start} - {end}"
        return formatted_string
    
    def login_and_go_to_patient_page_by_patient_number(self, login, setup_method, user_credentials, patient_list, patient_number: int, user: str) -> PatientPage:
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
    
    def go_to_first_upcoming_visit(self, patient_page: PatientPage) -> VisitPage:
        upcoming = patient_page.get_upcoming_visits()
        patient_page.click_on_detail_in_upcoming_visit(upcoming[0][0])
        visit_page = VisitPage(patient_page.driver, patient_page.base_url)
        return visit_page
    
    @pytest.mark.parametrize("user, visible", [
        ("receptionist", True),
        ("manager", True),
        ("doctor", False) 
    ])
    def test_visible_cancel_reserwation(self, login, setup_method, user_credentials, patient_list, user, visible):
        patient_number = random.randint(0,9)
        patient_page = self.login_and_go_to_patient_page_by_patient_number(login, setup_method, user_credentials, patient_list, patient_number, user)
        visit_page: VisitPage = self.go_to_first_upcoming_visit(patient_page)
        assert visit_page.visible_check_cancel_button() == visible
        
    def test_cancel_canceling_visit(self, login, setup_method, user_credentials, patient_list):
        patient_num = random.randint(0,9)
        user = random.choice(['receptionist', 'manager'])
        patient_page = self.login_and_go_to_patient_page_by_patient_number(login, setup_method, user_credentials, patient_list, patient_num, user)
        visit_page: VisitPage = self.go_to_first_upcoming_visit(patient_page)
        assert not visit_page.visible_check_cancel_confirmation()
        visit_page.click_on_cancel_button()
        time.sleep(0.5)
        assert visit_page.visible_check_cancel_confirmation()
        visit_page.click_on_close_on_cancel_confirmation()
        time.sleep(0.5)
        assert not visit_page.visible_check_cancel_confirmation()
        
    def test_cancel_visit(self, login, setup_method, user_credentials, patient_list, get_current_url):
        patient_num = random.randint(0,9)
        user = random.choice(['receptionist', 'manager'])
        patient_page = self.login_and_go_to_patient_page_by_patient_number(login, setup_method, user_credentials, patient_list, patient_num, user)
        visit_page: VisitPage = self.go_to_first_upcoming_visit(patient_page)
        visit_info = visit_page.get_basic_visit_info()
        print(visit_info, sep='|')
        visit_page.click_on_cancel_button()
        time.sleep(0.5)
        visit_page.click_on_yes_on_cancel_confirmation()
        time.sleep(0.5)
        assert '/patient/' in get_current_url(visit_page.driver)
        
        patient_page.select_visit_name_by_visit_name(visit_info[0])
        patient_page.select_doctor_by_fullname(visit_info[2].replace('Doctor: ',''))
        week = self.in_witch_week_is_date(visit_info[1])
        if week is None:
            assert False
        patient_page.select_week_by_visible_text(week)
        patient_page.click_on_search_button()
        time.sleep(0.5)
        visible = False
        days = patient_page.get_visible_days_from_days_nav_segment()
        for day in days:
            for visit in patient_page.get_visit_form_visit_section(day):
                if visit[3] == visit_info[0] and visit[5].replace('Doc. ', '') == visit_info[2].replace('Doctor: ', '') and self.transrofm_info_to_data_special(visit[4], visit[1], visit[2]) == visit_info[1]:
                    visible = True
        assert visible
         # sprawdzić wyświetlone wizyty czy jest ta która była odwołana
        
        
        
        
        
        
        
        
        