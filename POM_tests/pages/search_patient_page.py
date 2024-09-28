import time
from typing import List
from selenium import webdriver
from pages.navbar_page import NavbarPage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class SearchPatientPage(NavbarPage):
    
    def __init__(self, driver: webdriver, base_url: str) -> None:
        self.driver = driver
        self.base_url = base_url
        self.endpoint = 'patient/search/'
        
    def enter_first_name_in_patient_sherch(self, first_name: str) -> None:
        first_name_input = self.driver.find_element(By.ID, 'inputFirstName')
        first_name_input.clear()
        first_name_input.send_keys(first_name)
        
    def enter_last_name_in_patient_sherch(self, last_name: str) -> None:
        last_name_input = self.driver.find_element(By.ID, 'inputLastName')
        last_name_input.clear()
        last_name_input.send_keys(last_name)
        
    def enter_phone_in_patient_sherch(self, phone: str) -> None:
        phone_input = self.driver.find_element(By.ID, 'inputPhone')
        phone_input.clear()
        phone_input.send_keys(phone)
        
    def click_on_search_button(self) -> None:
        button = self.driver.find_element(By.ID, 'searchBtn')
        button.click()
        
    def get_patient_list(self) -> List[List]:
        time.sleep(1)
        patient_cards = self.driver.find_elements(By.CSS_SELECTOR, '.patient-info')
        print('ele:', len(patient_cards))
        patient_list = []
        for card in patient_cards:
            patient = []
            for id in ['name', 'birthDate', 'pesel', 'phone']:
                patient.append(card.find_element(By.ID, id).text)
            patient_list.append(patient)
        return patient_list

    def click_on_patient_profile(self, full_name: str) -> None:
        patient_cards = self.driver.find_elements(By.CSS_SELECTOR, 'patient-info')
        for card in patient_cards:
            if card.find_element(By.ID, 'name').text == full_name:
                profile_btn = card.find_element(By.ID, 'profileBtn')
                profile_btn.click()
                return