from typing import List
from selenium import webdriver
from pages.navbar_page import NavbarPage
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class DocEditVisitPage(NavbarPage):
    
    def __init__(self, driver: webdriver, base_url: str) -> None:
        self.driver = driver
        self.base_url = base_url
        self.endpoint = '/visit/id/doctor/edit'
        
    def get_basic_visit_info(self) -> List[str]:
        visit_card = self.driver.find_element(By.ID, 'visitInfo')
        basic_info = []
        for id in ['visitName', 'visitDate', 'patient', 'patient', 'visitTime', 'patientBirthday']:
            basic_info.append(visit_card.find_element(By.ID, id).text)
        return basic_info
    
    def get_description_text(self) -> str:
        return self.driver.find_element(By.ID, 'descArea').text
    
    def get_recommendation_text(self) -> str:
        return self.driver.find_element(By.ID, 'recoArea').text
    
    def insert_description_text(self, test: str) -> None:
        area = self.driver.find_element(By.ID, 'descArea')
        area.clear()
        area.send_keys(test)
    
    def insert_recomendation_text(self, test: str) -> None:
        area = self.driver.find_element(By.ID, 'recoArea')
        area.clear()
        area.send_keys(test)
        
    def is_passed_visit(self) -> bool:
        data = self.get_basic_visit_info()
        _, date_string = data[1].split(": ")
        start_time, end_time = data[4].split(" - ")
        start_datetime_str = f"{date_string} {start_time}"
        end_datetime_str = f"{date_string} {end_time}"
        datetime_format = "%d %B, %Y %H:%M"
        start_datetime = datetime.strptime(start_datetime_str, datetime_format)
        end_datetime = datetime.strptime(end_datetime_str, datetime_format)
        if end_datetime < datetime.now():
            return True
        return False
    
    def click_on_save_and_continue_button(self) -> None:
        self.driver.find_element(By.CSS_SELECTOR, '.sAc').click()
        
    def click_on_save_and_exit_button(self) -> None:
        self.driver.find_element(By.CSS_SELECTOR, '.sAe').click()
        
    def visible_check_save_and_continue_confirmation(self) -> bool:
        confirm = self.driver.find_element(By.ID, 'save_continue')
        return confirm.is_displayed()

        
    def visible_check_save_and_exit_confirmation(self) -> bool:
        confirm = self.driver.find_element(By.ID, 'save_exit')
        return confirm.is_displayed()

        
    def click_on_close_on_save_and_continue_confirmation(self) -> None:
        confirmation = self.driver.find_element(By.ID, 'save_continue')
        confirmation.find_element(By.ID, 'scClose').click()
    
    def click_on_ok_on_save_and_continue_confirmation(self) -> None:
        confirmation = self.driver.find_element(By.ID, 'save_continue')
        confirmation.find_element(By.ID, 'scAccept').click()
        
    def click_on_close_on_save_and_exit_confirmation(self) -> None:
        confirmation = self.driver.find_element(By.ID, 'save_exit')
        confirmation.find_element(By.ID, 'seClose').click()
        
    def click_on_ok_on_save_and_exit_confirmation(self) -> None:
        confirmation = self.driver.find_element(By.ID, 'save_exit')
        confirmation.find_element(By.ID, 'seAccept').click()