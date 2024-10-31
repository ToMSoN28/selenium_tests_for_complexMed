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
        
    def visible_check_delete_visit_button(self) -> bool:
        visit_card = self.driver.find_element(By.ID, 'visitInfo')
        try:
            visit_card.find_element(By.ID, 'delete')
            return True
        except NoSuchElementException:
            return False
        
    def click_on_cancel_button(self) -> None:
        visit_card = self.driver.find_element(By.ID, 'visitInfo')
        cancel_btn = visit_card.find_element(By.ID, 'cancel')
        cancel_btn.click()
        
    def visible_check_cancel_confirmation(self) -> bool:
        confirmation = self.driver.find_element(By.ID, 'cancelModal')
        return confirmation.is_displayed()
    
    def click_on_close_on_cancel_confirmation(self) -> None:
        confirmation = self.driver.find_element(By.ID, 'cancelModal')
        close_btn = confirmation.find_element(By.ID, 'closeCancel')
        close_btn.click()
        
    def click_on_yes_on_cancel_confirmation(self) -> None:
        confirmation = self.driver.find_element(By.ID, 'cancelModal')
        yes_btn = confirmation.find_element(By.ID, 'yesCancel')
        yes_btn.click()
        
    def click_on_delete_button(self) -> None:
        visit_card = self.driver.find_element(By.ID, 'visitInfo')
        delte_btn = visit_card.find_element(By.ID, 'delte')
        delte_btn.click()
        
    def visible_check_delete_confitmation(self) -> bool:
        confirmation = self.driver.find_element(By.ID, 'deleteModal')
        return confirmation.is_displayed()
        
    def click_on_close_on_delete_confirmation(self) -> None:
        confirmation = self.driver.find_element(By.ID, 'deleteModal')
        close_btn = confirmation.find_element(By.ID, 'closeDelete')
        close_btn.click()
        
    def click_on_yes_on_delete_confirmation(self) -> None:
        confirmation = self.driver.find_element(By.ID, 'deleteModal')
        yes_btn = confirmation.find_element(By.ID, 'yesDelete')
        yes_btn.click()
        
    def click_on_report_visit_btn(self) -> None:
        visit_card = self.driver.find_element(By.ID, 'visitInfo')
        report_btn = visit_card.find_element(By.ID, 'report')
        report_btn.click()
        
    def click_on_edit_report_button(self) -> None:
        visit_card = self.driver.find_element(By.ID, 'visitInfo')
        edit_btn = visit_card.find_element(By.ID, 'edit')
        edit_btn.click()
        
    def visible_check_edit_confirmation(self) -> None:
        confirmation = self.driver.find_element(By.ID, 'editModal')
        return confirmation.is_displayed()
    
    def click_on_close_on_edit_confirmation(self) -> None:
        confirmation = self.driver.find_element(By.ID, 'editModal')
        close_btn = confirmation.find_element(By.ID, 'closeEdit')
        close_btn.click()
        
    def click_on_yes_on_edit_confirmation(self) -> None:
        confirmation = self.driver.find_element(By.ID, 'editModal')
        yes_btn = confirmation.find_element(By.ID, 'yesEdit')
        yes_btn.click()
    
    def visible_check_visit_description(self) -> bool:
        try:
            desc_section = self.driver.find_element(By.ID, 'desc')
            return True
        except NoSuchElementException:
            return False
        
    def get_description_text(self) -> str:
        return self.driver.find_element(By.ID, 'DescriptionText').text
    
    def get_recommendation_text(self) -> str:
        return self.driver.find_element(By.ID, 'RecommendationText').text