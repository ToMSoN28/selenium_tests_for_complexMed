import time
from typing import List
from selenium import webdriver
from pages.navbar_page import NavbarPage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains



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
            patient.append(card.get_attribute('data-patient-id'))
            for id in ['name', 'birthDate', 'pesel', 'phone']:
                patient.append(card.find_element(By.ID, id).text)
            patient_list.append(patient)
        return patient_list

    def click_on_patient_profile(self, patient_id: str) -> None:
        patient_card = self.driver.find_element(By.XPATH, f'//*[@data-patient-id="{patient_id}"]')
        profile_btn = patient_card.find_element(By.ID, 'profileBtn')
        # is_in_viewport = self.driver.execute_script(
        #     "const rect = arguments[0].getBoundingClientRect();"
        #     "return (rect.top >= 0 && rect.left >= 0 && "
        #     "rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && "
        #     "rect.right <= (window.innerWidth || document.documentElement.clientWidth));", 
        #     profile_btn
        # )
        # print(is_in_viewport)
        # if not is_in_viewport:
        #     self.driver.execute_script("arguments[0].scrollIntoView();", profile_btn)
        #     self.driver.implicitly_wait(1)
        # profile_btn.click()
        ActionChains(self.driver).move_to_element(profile_btn).click().perform()
