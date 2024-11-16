import pytest
from typing import Tuple
from datetime import datetime
from pages.visit_page import VisitPage
from pages.doctor_dashboard_page import DoctorDashboardPage


class TestUC09:
    
    def login(self, login, setup_method, user_credentials, user: str) -> DoctorDashboardPage:
        user_l, user_p = user_credentials[user]
        login(user_l, user_p)
        driver, base_url = setup_method
        doctor_dashboard_page = DoctorDashboardPage(driver, base_url)
        return doctor_dashboard_page
    
    def transform_basic_date(self, date_str: str) -> Tuple[datetime]:
        date_part, time_part = date_str.split("     ")
        _, date_string = date_part.split(": ")
        start_time, end_time = time_part.split(" - ")
        start_datetime_str = f"{date_string} {start_time}"
        end_datetime_str = f"{date_string} {end_time}"
        datetime_format = "%d %B, %Y %H:%M"
        start_datetime = datetime.strptime(start_datetime_str, datetime_format)
        end_datetime = datetime.strptime(end_datetime_str, datetime_format)
        return start_datetime, end_datetime
    
    def test_doctor_has_upcoming_visit_today(self, login, setup_method, user_credentials):
        user = 'doctor'
        doctor_dashboard_page: DoctorDashboardPage = self.login(login, setup_method, user_credentials, user)
        doctor_dashboard_page.click_on_daily_visits()
        last_refresh = doctor_dashboard_page.get_data_and_time_from_doc_dasboard()
        if doctor_dashboard_page.visible_check_upcoming_visit():
            visit_page = VisitPage(doctor_dashboard_page.driver, doctor_dashboard_page.base_url)
            upcoming = doctor_dashboard_page.get_upcoming_visit_info()
            datetime_check = [last_refresh]
            for visit in upcoming:
                doctor_dashboard_page.click_on_detail_button(visit[0], 'u')
                visit_info = visit_page.get_basic_visit_info()
                assert visit[3] == visit_info[0]
                start, end = self.transform_basic_date(visit_info[1])
                assert start > last_refresh
                datetime_check.append(start)
                datetime_check.append(end)
                assert doctor_dashboard_page.get_worker_name() == visit_info[2].replace('Doctor: ', '')
                doctor_dashboard_page.driver.back()
            for i in range(len(datetime_check)-1):
                assert datetime_check[i] <= datetime_check[i+1]
                
    def test_doctor_has_passed_visit_today(self, login, setup_method, user_credentials):
        user = 'doctor'
        doctor_dashboard_page: DoctorDashboardPage = self.login(login, setup_method, user_credentials, user)
        doctor_dashboard_page.click_on_daily_visits()
        last_refresh = doctor_dashboard_page.get_data_and_time_from_doc_dasboard()
        if doctor_dashboard_page.visible_check_passed_visit():
            visit_page = VisitPage(doctor_dashboard_page.driver, doctor_dashboard_page.base_url)
            passed = doctor_dashboard_page.get_passed_visit_info()
            datetime_check = [last_refresh]
            for visit in passed:
                doctor_dashboard_page.click_on_detail_button(visit[0], 'p')
                visit_info = visit_page.get_basic_visit_info()
                assert visit[3] == visit_info[0]
                start, end = self.transform_basic_date(visit_info[1])
                assert start < last_refresh
                datetime_check.append(start)
                datetime_check.append(end)
                assert doctor_dashboard_page.get_worker_name() == visit_info[2].replace('Doctor: ', '')
                doctor_dashboard_page.driver.back()
            for i in range(len(datetime_check)-1):
                assert datetime_check[i] >= datetime_check[i+1]
                
                
                
    