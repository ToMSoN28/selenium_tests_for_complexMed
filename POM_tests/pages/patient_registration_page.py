import time
from pages.page import Page
from pages.navbar_page import NavbarPage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class PatientRegistrationPage(Page, NavbarPage):
    
    def __init__(self, driver, base_url: str) -> None:
        # super().__init__(driver, base_url)
        self.driver = driver
        self.base_url = base_url
        self.endpoint = 'patient-registration/'
        pass
    
    def open_patient_registration_page(self) -> None:
        self.driver.get(f'{self.base_url}{self.endpoint}')
    
    def enter_patient_first_name(self, first_name: str):
        first_name_input = self.driver.find_element(By.ID, 'inputFirstName')
        first_name_input.clear()
        first_name_input.send_keys(first_name)
    
    def enter_patient_last_name(self, last_name: str):
        last_name_input = self.driver.find_element(By.ID, 'inputLastName')
        last_name_input.clear()
        last_name_input.send_keys(last_name)
        
    
    def enter_patient_pesel(self, pesel: str):
        pesel_input = self.driver.find_element(By.ID, 'inputPesel')
        pesel_input.clear()
        pesel_input.send_keys(pesel)
    
    def enter_patient_phone_number(self, phone_number: str):
        phone_number_input = self.driver.find_element(By.ID, 'inputPhoneNumber')
        phone_number_input.clear()
        phone_number_input.send_keys(phone_number)
    
    def click_on_register_button(self):
        button = self.driver.find_element(By.ID, 'buttonRegister')
        button.click()
        
    def check_error_message(self):
        error_msg = self.driver.find_element(By.ID, 'errorMsg')
        return error_msg.text