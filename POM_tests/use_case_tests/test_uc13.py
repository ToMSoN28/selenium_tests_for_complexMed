import time
import pytest
import random
from datetime import datetime, timedelta
from pages.patient_page import PatientPage
from pages.search_patient_page import SearchPatientPage


class TestUC13:
    
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
    
    @pytest.mark.parametrize("user, expected", [
        ('doctor', False),
        ('manager', True),
        ('receptionist', True)
    ])
    def test_visible_search_available_visit_module(self, login, setup_method, user_credentials, patient_list, user: str, expected: bool):
        patient_num = random.randint(0,9)
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, patient_num, user)
        time.sleep(0.5)
        assert patient_page.visible_check_search_available_visit_panel() == expected
    
    @pytest.mark.parametrize("user", [
        ('manager'),
        ('receptionist')
    ])    
    def test_choose_visit_name_in_search_visit_module(self, login, setup_method, user_credentials, patient_list, visit_name_list, user):
        patient_num = random.randint(0,9)
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, patient_num, user)
        time.sleep(0.5)
        visit_name_options = patient_page.get_available_visit_names()
        for visit_name in visit_name_options[1:]:
            assert visit_name.text in visit_name_list
    
    @pytest.mark.parametrize("user", [
        ('manager'),
        ('receptionist')
    ])
    def test_choose_doctor_in_search_visit_module(self, login, setup_method, user_credentials, patient_list, doctors_list, user):
        patient_num = random.randint(0,9)
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, patient_num, user)
        time.sleep(0.5)
        doctors = patient_page.get_available_doctors()
        for doctor in doctors[1:]:
            assert doctor.text in doctors_list
            
    @pytest.mark.parametrize("user", [
        ('manager'),
        ('receptionist')
    ])
    def test_choose_weeks_in_search_visit_module(self, login, setup_method, user_credentials, patient_list, user):
        patient_num = random.randint(0,9)
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, patient_num, user)
        time.sleep(0.5)
        weeks = patient_page.get_available_weeks()
        for week in weeks[1:]:
            assert week.text in self.weeks        
            
    @pytest.mark.parametrize("visit_name_num, doctor_num, week_num", [
        (None, None, 1),
        (None, 1, 1),
        (4, None, 2)
    ])
    def test_filtring_available_visit(self, login, setup_method, user_credentials, patient_list, doctors_list, visit_name_list, doctor_num: int, visit_name_num: int, week_num: int):
        patient_num = random.randint(0,9)
        user = random.choice(['receptionist', 'manager'])
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, patient_num, user)
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
                assert f'Doc. {doctors_list[doctor_num]}' == visit[5]
            assert self.is_workday_in_week(visit[4], week_num)   
            
    def test_cancel_assigning_patient(self, login, setup_method, user_credentials, patient_list):
        patient_num = random.randint(0,9)
        user = random.choice(['receptionist', 'manager'])
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, patient_num, user)
        patient_page.select_week_by_visible_text(self.weeks[1])
        patient_page.click_on_search_button()
        available_visits = patient_page.get_visit_form_visit_section('link-1')
        visit_id = available_visits[0][0]
        assert not patient_page.visible_check_assign_confirmation(visit_id)
        patient_page.click_on_assing_button_on_visit(visit_id)
        time.sleep(0.5)
        assert patient_page.visible_check_assign_confirmation(visit_id)
        assert f'Assign {patient_list[patient_num]['first_name']} {patient_list[patient_num]['last_name']} for {available_visits[0][3]}' == patient_page.get_text_on_confirmation(visit_id)
        patient_page.click_on_close_confirmation_button(visit_id)
        time.sleep(0.5)
        assert not patient_page.visible_check_assign_confirmation(visit_id)     
        
    def test_assigning_patient(self, login, setup_method, user_credentials, patient_list):
        patient_num = random.randint(0,9)
        user = random.choice(['receptionist', 'manager'])
        patient_page = self.login_and_go_to_patien_page_by_patient_number(login, setup_method, user_credentials, patient_list, patient_num, user)
        patient_page.select_week_by_visible_text(self.weeks[1])
        patient_page.click_on_search_button()
        available_visits = patient_page.get_visit_form_visit_section('link-1')
        visit_id = available_visits[0][0]
        print(available_visits[0])
        patient_page.click_on_assing_button_on_visit(visit_id)
        time.sleep(0.5)
        patient_page.click_on_assign_confirmatino_button(visit_id)
        time.sleep(0.5)
        upcoming = patient_page.get_upcoming_visits()
        correct_assigning = False
        for visit in upcoming:
            if visit[0] == available_visits[0][0] and visit[1] == available_visits[0][3] and visit[2] == available_visits[0][4] and visit[3] == f'{available_visits[0][1]} - {available_visits[0][2]}' and visit[4] == available_visits[0][5]:
                    correct_assigning = True
                    print(visit)
        assert correct_assigning
                    
            
     