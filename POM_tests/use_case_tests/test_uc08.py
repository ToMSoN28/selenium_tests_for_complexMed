import pytest
from datetime import datetime
from pages.visit_page import VisitPage
from pages.doctor_dashboard_page import DoctorDashboardPage


class TestUC08: # wyświetlenie aktualnej wizyty
    
    def login(self, login, setup_method, user_credentials, user: str) -> DoctorDashboardPage:
        user_l, user_p = user_credentials[user]
        login(user_l, user_p)
        driver, base_url = setup_method
        doctor_dashboard_page = DoctorDashboardPage(driver, base_url)
        return doctor_dashboard_page
    
    def test_visible_actual_visit_panel(self, login, setup_method, user_credentials):
        user = 'doctor'
        doctor_dashboard_page: DoctorDashboardPage = self.login(login, setup_method, user_credentials, user)
        doctor_dashboard_page.click_on_daily_visits()
        assert doctor_dashboard_page.visible_check_actual_visit()
        
    def test_actula_visit_if_exist(self, login, setup_method, user_credentials, get_current_url):
        user = 'doctor'
        doctor_dashboard_page: DoctorDashboardPage = self.login(login, setup_method, user_credentials, user)
        doctor_dashboard_page.click_on_daily_visits()
        now  = datetime.now()
        now = now.replace(second=0, microsecond=0)
        if doctor_dashboard_page.has_actual_visit():
            visit = doctor_dashboard_page.get_info_of_actual_visit()
            print(visit)
            start_time_str, end_time_str = visit[1].split(" - ")
            start_time = datetime.strptime(start_time_str, "%H:%M").time()
            end_time = datetime.strptime(end_time_str, "%H:%M").time()
            now = now.time()
            assert start_time <= now
            assert end_time >= now
            doctor_dashboard_page.click_on_detail_on_actual_visit()
            visit_page = VisitPage(doctor_dashboard_page.driver, doctor_dashboard_page.base_url)
            visit_info = visit_page.get_basic_visit_info()
            assert visit[3] == visit_info[3]
            assert visit[2] == visit_info[4]
            assert doctor_dashboard_page.get_worker_name() == visit_info[2].replace('Doctor: ', '')
            assert visit[0] == visit_info[0]
            
            
            
            
            
            
        
    