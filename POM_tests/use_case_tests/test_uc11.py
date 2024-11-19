import pytest
import time, random
from datetime import datetime
from pages.visit_page import VisitPage
from pages.patient_page import PatientPage
from pages.search_patient_page import SearchPatientPage
from pages.doc_edit_visit_page import DocEditVisitPage
from pages.doctor_dashboard_page import DoctorDashboardPage

class TestUC11:
    
    def login(self, login, setup_method, user_credentials, user: str) -> DoctorDashboardPage:
        user_l, user_p = user_credentials[user]
        login(user_l, user_p)
        driver, base_url = setup_method
        # doctor_dashboard_page = DoctorDashboardPage(driver, base_url)
        return driver, base_url
    
    def go_to_patient_page(self, driver, base_url) -> PatientPage:
        search_patient_page = SearchPatientPage(driver, base_url)
        search_patient_page.click_on_search_patient()
        time.sleep(0.5)
        search_patient_page.click_on_search_button()
        patient_info_list = search_patient_page.get_patient_list()
        print(patient_info_list)
        patient_id = random.choices(patient_info_list)
        print(patient_id)
        patient_id = patient_id[0][0]
        print(patient_id)
        search_patient_page.click_on_patient_profile(patient_id)
        patient_page = PatientPage(driver, base_url)
        return patient_page
    
    @pytest.mark.parametrize("user", [
        ("receptionist"),
        ("manager"),
        ("doctor") 
    ])
    def test_visible_button_to_edit_visit_description(self, login, setup_method, user_credentials, user):
        driver, base_url = self.login(login, setup_method, user_credentials, user)
        patient_page: PatientPage = self.go_to_patient_page(driver, base_url)
        upcoming = patient_page.get_upcoming_visits()
        visit_page = VisitPage(driver, base_url)
        for upcoming_visit in upcoming:
            patient_page.click_on_detail_in_upcoming_visit(upcoming_visit[0])
            time.sleep(0.5)
            assert not visit_page.visible_check_edit_report_button()
            assert not visit_page.visible_check_report_visit_button()
            patient_page.driver.back()
        past = patient_page.get_past_visits()
        for past_visit in past:
            patient_page.click_on_detail_in_past_visit(past_visit[0])
            time.sleep(0.5)
            if visit_page.get_basic_visit_info()[2].replace('Doctor: ', '') == visit_page.get_worker_name():
                assert visit_page.visible_check_edit_report_button()
            else:
                assert not visit_page.visible_check_edit_report_button()
            assert not visit_page.visible_check_report_visit_button()
            patient_page.driver.back()
            
    def test_edit_past_visit(self, login, setup_method, user_credentials, get_current_url):
        user = 'doctor'
        driver, base_url = self.login(login, setup_method, user_credentials, user)
        doc_dasboard = DoctorDashboardPage(driver, base_url)
        past_visits = doc_dasboard.get_passed_visit_info()
        visit_page = VisitPage(driver, base_url)
        edit_visit_page = DocEditVisitPage(driver, base_url)
        for past in past_visits:
            if past[4] != 'Patient:':
                doc_dasboard.click_on_detail_button(past[0], 'p')
                assert not visit_page.visible_check_edit_confirmation()
                visit_page.click_on_edit_report_button()
                time.sleep(0.3)
                assert visit_page.visible_check_edit_confirmation()
                visit_page.click_on_close_on_edit_confirmation()
                time.sleep(0.3)
                assert not visit_page.visible_check_edit_confirmation()
                desc = visit_page.get_description_text()
                reco = visit_page.get_recommendation_text()
                visit_page.click_on_edit_report_button()
                time.sleep(0.3)
                visit_page.click_on_yes_on_edit_confirmation()
                assert get_current_url(driver) == edit_visit_page.endpoint.replace('id', past[0].replace('visit', ''))
                assert desc == edit_visit_page.get_description_text()
                assert reco == edit_visit_page.get_recommendation_text()
                edit_visit_page.insert_description_text('desc_test1')
                edit_visit_page.insert_recomendation_text('reco_test1')
                assert not edit_visit_page.visible_check_save_and_continue_confirmation()
                edit_visit_page.click_on_save_and_continue_button()
                time.sleep(0.3)
                assert edit_visit_page.visible_check_save_and_continue_confirmation()
                edit_visit_page.click_on_ok_on_save_and_continue_confirmation()
                edit_visit_page.click_on_daily_visits()
                doc_dasboard.click_on_detail_button(past[0], 'p')
                time.sleep(0.2)
                assert 'desc_test1' == visit_page.get_description_text()
                assert 'reco_test1' == visit_page.get_recommendation_text()
                visit_page.click_on_edit_report_button()
                time.sleep(0.3)
                visit_page.click_on_yes_on_edit_confirmation()
                assert 'desc_test1' == edit_visit_page.get_description_text()
                assert 'reco_test1' == edit_visit_page.get_recommendation_text()
                # assert not edit_visit_page.visible_check_save_and_continue_confirmation()
                edit_visit_page.insert_description_text('desc_test2')
                edit_visit_page.insert_recomendation_text('reco_test2')
                assert not edit_visit_page.visible_check_save_and_exit_confirmation()
                edit_visit_page.click_on_save_and_exit_button()
                time.sleep(0.3)
                assert edit_visit_page.visible_check_save_and_exit_confirmation()
                edit_visit_page.click_on_ok_on_save_and_exit_confirmation()
                assert 'desc_test2' == visit_page.get_description_text()
                assert 'reco_test2' == visit_page.get_recommendation_text()
                
    def test_edit_actual_visit(self, login, setup_method, user_credentials, get_current_url):
        user = 'doctor'
        driver, base_url = self.login(login, setup_method, user_credentials, user)
        doc_dasboard = DoctorDashboardPage(driver, base_url)
        visit_page = VisitPage(driver, base_url)
        edit_visit_page = DocEditVisitPage(driver, base_url)
        if doc_dasboard.has_actual_visit():
            doc_dasboard.click_on_detail_on_actual_visit()
            desc = visit_page.get_description_text()
            reco = visit_page.get_recommendation_text()
            end_visit = get_current_url(driver)
            visit_page.click_on_report_visit_btn()
            assert get_current_url(driver) == f'{end_visit}{edit_visit_page.endpoint.replace('/visit/id/', '')}'
            assert desc == edit_visit_page.get_description_text()
            assert reco == edit_visit_page.get_recommendation_text()
            edit_visit_page.insert_description_text('desc_test1')
            edit_visit_page.insert_recomendation_text('reco_test1')
            edit_visit_page.click_on_save_and_continue_button()
            edit_visit_page.click_on_daily_visits()
            time.sleep(0.2)
            doc_dasboard.click_on_detail_on_actual_visit()
            time.sleep(0.2)
            assert 'desc_test1' == visit_page.get_description_text()
            assert 'reco_test1' == visit_page.get_recommendation_text()
            visit_page.click_on_report_visit_btn()
            assert 'desc_test1' == edit_visit_page.get_description_text()
            assert 'reco_test1' == edit_visit_page.get_recommendation_text()
            edit_visit_page.insert_description_text('desc_test2')
            edit_visit_page.insert_recomendation_text('reco_test2')
            edit_visit_page.click_on_save_and_exit_button()
            time.sleep(0.2)
            assert 'desc_test2' == visit_page.get_description_text()
            assert 'reco_test2' == visit_page.get_recommendation_text()
                
                
                
                
                
    