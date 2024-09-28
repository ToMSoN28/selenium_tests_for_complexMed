import time
from typing import List
from selenium import webdriver
from pages.navbar_page import NavbarPage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class WorkerListPage(NavbarPage):
    
    def __init__(self, driver: webdriver, base_url: str ) -> None:
        self.driver = driver
        self.base_url = base_url
        self.endpoint = 'workers-list/'
        
    def enter_first_name_in_worker_sherch(self, first_name: str) -> None:
        first_name_input = self.driver.find_element(By.ID, 'inputFirstName')
        first_name_input.clear()
        first_name_input.send_keys(first_name)
        
    def enter_last_name_in_worker_sherch(self, last_name: str) -> None:
        last_name_input = self.driver.find_element(By.ID, 'inputLastName')
        last_name_input.clear()
        last_name_input.send_keys(last_name)
        
    def enter_username_in_worker_sherch(self, username: str) -> None:
        username_input = self.driver.find_element(By.ID, 'inputUsername')
        username_input.clear()
        username_input.send_keys(username)
        
    def click_on_search_button(self) -> None:
        button = self.driver.find_element(By.ID, 'searchBtn')
        button.click()
        
    def get_workers_list(self) -> List[List]: 
        time.sleep(1)
        worker_cards = self.driver.find_elements(By.CSS_SELECTOR, '.worker-desc')
        workers_list = []
        for card in worker_cards:
            name = card.find_element(By.ID, 'name').text
            username = card.find_element(By.ID, 'username').text
            try:
                manager_svg = card.find_element(By.CSS_SELECTOR, "#isManager svg")
                is_manager = manager_svg.is_displayed()  # Sprawdza, czy jest widoczny
            except NoSuchElementException:
                is_manager = False
            try:
                doctor_svg = card.find_element(By.CSS_SELECTOR, "#isDoctor svg")
                is_doctor = doctor_svg.is_displayed()
            except NoSuchElementException:
                is_doctor = False
            try:
                receptionist_svg = card.find_element(By.CSS_SELECTOR, "#isReceptionist svg")
                is_receptionist = receptionist_svg.is_displayed()
            except NoSuchElementException:
                is_receptionist = False            
            workers_list.append([name, username, is_manager, is_doctor, is_receptionist])
        return workers_list

            
    
    