import pytest
from datetime import datetime
from pages.doctor_dashboard_page import DoctorDashboardPage


class TestUC07: # wyświetlenie dziennego grafiku
    
    def login(self, login, setup_method, user_credentials, user: str) -> DoctorDashboardPage:
        user_l, user_p = user_credentials[user]
        login(user_l, user_p)
        driver, base_url = setup_method
        doctor_dashboard_page = DoctorDashboardPage(driver, base_url)
        return doctor_dashboard_page
    
    @pytest.mark.parametrize("user, visible", [
        ("receptionist", False),
        ("manager", False),
        ("doctor", True) 
    ])
    def test_visible_of_doctor_dashboard(self, login, setup_method, user_credentials, get_current_url, user, visible):
        doctor_dashboard_page: DoctorDashboardPage = self.login(login, setup_method, user_credentials, user)
        assert doctor_dashboard_page.visible_check_daily_visits() == visible
        if visible:
            doctor_dashboard_page.click_on_daily_visits()
            assert get_current_url(doctor_dashboard_page.driver) == '/dashboard/doctor/'
            
    def test_last_refresh_on_dashboard(self, login, setup_method, user_credentials):
        user = 'doctor'
        doctor_dashboard_page: DoctorDashboardPage = self.login(login, setup_method, user_credentials, user)
        doctor_dashboard_page.click_on_daily_visits()
        last_refresh = doctor_dashboard_page.get_data_and_time_from_doc_dasboard()
        now  = datetime.now()
        now = now.replace(second=0, microsecond=0)
        assert last_refresh == now