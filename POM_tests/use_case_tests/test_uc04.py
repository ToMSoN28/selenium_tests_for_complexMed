import pytest
from pages.patient_page import PatientPage
from pages.search_patient_page import SearchPatientPage

class TestUC04: #Wyświetlenie profilu pacjenta
        
    def login_and_go_to_search_patient(self, login, setup_method, user_credentials, user: str):
        user_l, user_p = user_credentials[user]
        login(user_l, user_p)
        driver, base_url = setup_method
        search_patient_page = SearchPatientPage(driver, base_url)
        search_patient_page.click_on_search_patient()
        return search_patient_page
    
    @pytest.mark.parametrize("user", [
        ("manager"),
        ("doctor"),
        ("receptionist")
    ])
    def test_search_and_go_to_patient_profile(self, login, setup_method, user_credentials, get_current_url, user):
        search_patient_page = self.login_and_go_to_search_patient(login, setup_method, user_credentials, user)
        search_patient_page.click_on_search_button()
        patients_list = search_patient_page.get_patient_list()
        print(patients_list)
        for patient in patients_list:
            patient_id: str = patient[0]
            search_patient_page.click_on_patient_profile(patient_id)
            current_endpoint = get_current_url(search_patient_page.driver)
            assert current_endpoint == f'/patient/{patient_id.replace('patient', '')}/'
            patient_page = PatientPage(search_patient_page.driver, search_patient_page.base_url)
            patient_info = patient_page.get_patient_information()
            assert patient[1:] == patient_info
            search_patient_page.driver.back()