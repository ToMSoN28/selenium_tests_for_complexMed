from typing import List
from selenium import webdriver
from pages.navbar_page import NavbarPage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class VisitPage(NavbarPage):
    
    def __init__(self, driver: webdriver, base_url: str) -> None:
        self.driver = driver
        self.base_url = base_url
        self.endpoint = 'visit/id/'
        
    def get_basic_visit_info(self) -> List[str]:
        visit_card = self.driver.find_element(By.ID, 'visitInfo')
        basic_info = []
        for id in ['visitName', 'visitTime', 'doctor', 'patient', 'room', 'price']:
            basic_info.append(visit_card.find_element(By.ID, id))
        return basic_info
    
    def visible_check_cancel_button(self) -> bool:
        visit_card = self.driver.find_element(By.ID, 'visitInfo')
        try:
            visit_card.find_element(By.ID, 'cancel')
            return True
        except NoSuchElementException:
            return False
        
    def visible_check_report_visit_button(self) -> bool:
        visit_card = self.driver.find_element(By.ID, 'visitInfo')
        try:
            visit_card.find_element(By.ID, 'report')
            return True
        except NoSuchElementException:
            return False
        
    def visible_check_edit_report_button(self) -> bool:
        visit_card = self.driver.find_element(By.ID, 'visitInfo')
        try:
            visit_card.find_element(By.ID, 'edit')
            return True
        except NoSuchElementException:
            return False
        
    def click_on_cancel_button(self) -> None:
        visit_card = self.driver.find_element(By.ID, 'visitInfo')
        cancel_btn = visit_card.find_element(By.ID, 'cancel')
        cancel_btn.click()
        
    def visible_check_cancel_confirmation(self) -> bool:
        visit_card = self.driver.find_element(By.ID, 'visitInfo')
        confirmation = visit_card.find_element(By.ID, 'cancelModal')
        return confirmation.is_displayed()
    
    def click_on_close_on_cancel_confirmation(self) -> None:
        visit_card = self.driver.find_element(By.ID, 'visitInfo')
        confirmation = visit_card.find_element(By.ID, 'cancelModal')
        close_btn = confirmation.find_element(By.ID, 'closeCancel')
        close_btn.click()
        
    def click_on_yes_on_cancel_confirmation(self) -> None:
        visit_card = self.driver.find_element(By.ID, 'visitInfo')
        confirmation = visit_card.find_element(By.ID, 'cancelModal')
        yes_btn = confirmation.find_element(By.ID, 'yesCancel')
        yes_btn.click()
        
        
        
    