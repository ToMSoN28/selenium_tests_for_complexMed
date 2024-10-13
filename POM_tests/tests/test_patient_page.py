import time
import pytest
import random
from dateutil import parser
from typing import List, Tuple
from datetime import datetime, timedelta
from pages.patient_page import PatientPage
from pages.search_patient_page import SearchPatientPage


class TestPatientPage:
    
    weeks = [
        'This week',
        'Next week',
        'In two weeks'
    ]
    
    def is_workday_in_week(self, date_str: str, week_num: int) -> bool:
        date = datetime.strptime(date_str, '%b. %d, %Y').date()
        today = datetime.today().date()
        start_of_week = today - timedelta(days=today.weekday())
        target_week_start = start_of_week + timedelta(weeks=week_num)
        target_week_end = target_week_start + timedelta(days=4)
        print(target_week_start, target_week_end)
        if target_week_start <= date <= target_week_end and date.weekday() < 5:
            return True
        else:
            return False
        
    def create_time_interval(self, date_str: str, time_range: str) -> Tuple[datetime, datetime]:
        date_str = date_str.replace('.', '').strip()
        date = parser.parse(date_str)
        print(f'prase date: {date}')
        start_time_str, end_time_str = time_range.split(' - ')
        start_datetime = datetime.combine(date.date(), datetime.strptime(start_time_str.strip(), '%H:%M').time())
        end_datetime = datetime.combine(date.date(), datetime.strptime(end_time_str.strip(), '%H:%M').time())
        return start_datetime, end_datetime
    
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
            time.sleep(0.5)
            assert patient_page.visible_check_dayli_visits_section(day)
    
    @pytest.mark.parametrize("visit_name_num, doctor_num, week_num", [
        (None, None, 1),
        (None, 1, 1),
        (4, None, 2)
    ])
    def test_filtring_available_visit(self, login, setup_method, user_credentials, patient_list, doctors_list, visit_name_list, doctor_num: int, visit_name_num: int, week_num: int):
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, 5)
        if visit_name_num is not None:
            patient_page.select_visit_name_by_visit_name(visit_name_list[visit_name_num])
        if doctor_num is not None:
            patient_page.select_doctor_by_fullname(doctors_list[doctor_num])
        if week_num != 0:
            patient_page.select_week_by_visible_text(self.weeks[week_num])
        patient_page.click_on_search_button()
        time.sleep(0.5)
        available_days = patient_page.get_visible_days_from_days_nav_segment()
        available_visits = []
        for day in available_days:
            available_visits.extend(patient_page.get_visit_form_visit_section(day))
        print(available_visits)
        for visit in available_visits:
            if visit_name_num is not None:
                assert visit_name_list[visit_name_num] == visit[3]
            if doctor_num is not None:
                assert f'Dr. {doctors_list[doctor_num]}' == visit[5]
            assert self.is_workday_in_week(visit[4], week_num)        
        
    def test_fail_assigning_confirmation(self, login, setup_method, user_credentials, patient_list):
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, 5)
        patient_page.select_week_by_visible_text(self.weeks[1])
        patient_page.click_on_search_button()
        available_visits = patient_page.get_visit_form_visit_section('link-1')
        visit_id = available_visits[0][0]
        assert not patient_page.visible_check_assign_confirmation(visit_id)
        patient_page.click_on_assing_button_on_visit(visit_id)
        time.sleep(0.5)
        assert patient_page.visible_check_assign_confirmation(visit_id)
        assert f'Assign {patient_list[5]['first_name']} {patient_list[5]['last_name']} for {available_visits[0][3]}' == patient_page.get_text_on_confirmation(visit_id)
        patient_page.click_on_close_confirmation_button(visit_id)
        time.sleep(0.5)
        assert not patient_page.visible_check_assign_confirmation(visit_id)
        
    def test_visible_upcoming_and_past_visits(self, login, setup_method, user_credentials, patient_list):
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, 5)
        assert patient_page.visible_check_past_visits()
        assert patient_page.visible_check_upcoming_visits()
        
    def test_upcoming_and_past_visit_information(self, login, setup_method, user_credentials, patient_list):
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, 5)
        past = patient_page.get_past_visits()
        print(past)
        past_datatime = []
        for v in past:
            past_datatime.append(self.create_time_interval(v[2], v[3]))
        for i in range(len(past)-1):
            assert past_datatime[i][0] > past_datatime[i+1][0]
        upcoming = patient_page.get_upcoming_visits()
        print(upcoming)
        upcoming_datatime = []
        for v in upcoming:
            upcoming_datatime.append(self.create_time_interval(v[2], v[3]))
        for i in range(len(upcoming)-1):
            assert upcoming_datatime[i][0] < upcoming_datatime[i+1][0]
            
    def test_redirection_aftec_click_on_detal_in_upcoming_or_past_visit(self, login, setup_method, user_credentials, patient_list, get_current_url):
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, 5)
        past = patient_page.get_past_visits()
        past_visit = random.choice(past)
        patient_page.click_on_detail_in_past_visit(past_visit[0])
        past_num = past_visit[0].replace("visit",'')
        assert f'/visit/{past_num}/' == get_current_url(patient_page.driver)
        patient_page.driver.back()
        upcoming = patient_page.get_past_visits()
        upcoming_visit = random.choice(upcoming)
        patient_page.click_on_detail_in_past_visit(past_visit[0])
        upcoming_num = upcoming_visit[0].replace("visit",'')
        assert f'/visit/{upcoming_num}/' == get_current_url(patient_page.driver)
        
    def test_success_assiging_to_visist(self, login, setup_method, user_credentials, patient_list):
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, 5)
        patient_page.select_week_by_visible_text(self.weeks[1])
        patient_page.click_on_search_button()
        available_visits = patient_page.get_visit_form_visit_section('link-1')
        visit= available_visits[0]
        patient_page.click_on_assing_button_on_visit(visit[0])
        patient_page.click_on_assign_confirmatino_button(visit[0])
        patient_page.click_on_search_button()
        available_visits = patient_page.get_visit_form_visit_section('link-1')
        assert visit not in available_visits
        upcoming = patient_page.get_upcoming_visits()
        v_visit = [visit[0], visit[3], visit[4], f'{visit[1]} - {visit[2]}', visit[5], True]
        assert v_visit in upcoming
        
        
        
    
        
        
        
        