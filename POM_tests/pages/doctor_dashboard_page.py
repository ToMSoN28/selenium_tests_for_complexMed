from typing import List, Literal
from selenium import webdriver
from pages.navbar_page import NavbarPage
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


class DoctorDashboardPage(NavbarPage):
    
    def __init__(self, driver: webdriver, base_url: str) -> None:
        self.driver = driver
        self.base_url = base_url
        self.endpoint = 'patient/id/'
        
    def get_data_and_time_from_doc_dasboard(self) -> datetime:
        dashboard_card = self.driver.find_element(By.ID, 'dailyDashboard')
        date_str = dashboard_card.find_element(By.ID, 'date').text
        time_str = dashboard_card.find_element(By.ID, 'time').text
        datetime_str = f'{date_str} {time_str.replace('Last refresh: ', '')}'
        dt = datetime.strptime(datetime_str, "%B %d, %Y %H:%M")
        return dt
    
    def visible_check_actual_visit(self) -> bool:
        try:
            self.driver.find_element(By.ID, 'actualVisit')
            return True
        except NoSuchElementException:
            return False
        
    def has_actual_visit(self) -> bool:
        try:
            actual_visit = self.driver.find_element(By.ID, 'actualVisit')
            info_party = actual_visit.find_element(By.CSS_SELECTOR, '.card-text')
            return True
        except NoSuchElementException:
            return False
        
    def get_info_of_actual_visit(self) -> List[str]:
        actual_visit = self.driver.find_element(By.ID, 'actualVisit')
        info_party = actual_visit.find_element(By.CSS_SELECTOR, '.card-text')
        info = []
        for id in ['aName','aTime','aRoom','aPatient']:
            info.append(info_party.find_element(By.ID, id).text)
        info.append(info_party.find_element(By.ID, 'aDetail').is_displayed())
        return info
    
    def click_on_detail_on_actual_visit(self) -> None:
        actual_visit = self.driver.find_element(By.ID, 'actualVisit')
        info_party = actual_visit.find_element(By.CSS_SELECTOR, '.card-text')
        buttton = info_party.find_element(By.ID, 'aDetail')
        buttton.click()
        
    def visible_check_upcoming_visit(self) -> bool:
        try:
            upcoming = self.driver.find_elements(By.CSS_SELECTOR, '.upcoming')
            return True
        except NoSuchElementException:
            return False
        
    def visible_check_passed_visit(self) -> bool:
        try:
            passed = self.driver.find_elements(By.CSS_SELECTOR, '.passed')
            return True
        except NoSuchElementException:
            return False
        
    def get_upcoming_visit_info(self) -> List[str]:
        upcoming = self.driver.find_elements(By.CSS_SELECTOR, '.upcoming')
        result = []
        for visit in upcoming:
            tmp = [visit.get_attribute('id')]
            for id in ['uStartTime','uEndTime','uVisitName','uPatient']:
                tmp.append(visit.find_element(By.ID, id).text)
            result.append(tmp)
        return result
    
    def get_passed_visit_info(self) -> List[str]:
        passed = self.driver.find_elements(By.CSS_SELECTOR, '.passed')
        result = []
        for visit in passed:
            tmp = [visit.get_attibute('id')]
            for id in ['pStartTime','pEndTime','pVisitName','pPatient']:
                tmp.append(visit.find_element(By.ID, id).text)
            result.append(tmp)
        return result
         
    def click_on_detail_button(self, visit_id: str, upPas: Literal['p', 'u']) -> None:
        visit_card = self.driver.find_element(By.ID, visit_id)
        detail_btn = visit_card.find_element(By.ID, f'{upPas}Detail')
        ActionChains(self.driver).move_to_element(detail_btn).click().perform()    
        
    