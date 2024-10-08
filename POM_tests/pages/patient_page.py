import time
from typing import List
from selenium import webdriver
from pages.navbar_page import NavbarPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


class PatientPage(NavbarPage):
    
    def __init__(self, driver: webdriver, base_url: str) -> None:
        self.driver = driver
        self.base_url = base_url
        self.endpoint = 'patient/id/'
        
    def get_patient_information(self) -> List[str]:
        patient_card = self.driver.find_element(By.CSS_SELECTOR, '.patient-info')
        patient = []
        for id in ['name', 'birthDate', 'pesel', 'phone']:
            patient.append(patient_card.find_element(By.ID, id).text)
        return patient
    
    def visible_check_search_available_visit_panel(self) -> bool:
        try:
            search_panel = self.driver.find_element(By.CSS_SELECTOR, '.available-visit-panel')
            return True
        except NoSuchElementException:
            return False
        
    def get_available_visit_names(self) -> Select.options:   # option.text
        visit_name_dropdown = Select(self.driver.find_element(By.ID, 'selectName'))
        return visit_name_dropdown.options
        
    def select_visit_name_by_visit_name(self, visit_name: str) -> None:
        visit_name_dropdown = Select(self.driver.find_element(By.ID, 'selectName'))
        visit_name_dropdown.select_by_visible_text(visit_name)
        
    def get_available_doctors(self) -> Select.options:
        doctor_fullname_dropdown = Select(self.driver.find_element(By.ID, 'selectDoctor'))
        return doctor_fullname_dropdown.options
    
    def select_doctor_by_fullname(self, doctor_fullname: str) -> None:
        doctor_fullname_dropdown = Select(self.driver.find_element(By.ID, 'selectDoctor'))
        doctor_fullname_dropdown.select_by_visible_text(doctor_fullname)
    
    def get_available_weeks(self) -> Select.options:
        week_dropdown = Select(self.driver.find_element(By.ID, 'selectWeek'))
        return week_dropdown.options
        
    def select_week_by_visible_text(self, week_text: str) -> None:
        week_dropdown = Select(self.driver.find_element(By.ID, 'selectWeek'))
        week_dropdown.select_by_visible_text(week_text)
        
    def click_on_search_button(self) -> None:
        button = self.driver.find_element(By.ID, 'searchBtn')
        button.click()
        
    def visible_check_days_navigation_segment(self) -> bool:
        try:
            days_nav = self.driver.find_element(By.CSS_SELECTOR, '.nav-items')
            return True
        except NoSuchElementException:
            return False
        
    def get_visible_days_from_days_nav_segment(self) -> List[str]:
        days_nav = self.driver.find_element(By.CSS_SELECTOR, '.nav-items')
        visible_days = days_nav.find_elements(By.CLASS_NAME, 'nav-link')
        result = []
        for day in visible_days:
            result.append(day.get_attribute("id"))
        return result
    
    def click_on_day_from_days_nav_segment(self, day_id:str) -> None:
        day_link = self.driver.find_element(By.ID, day_id)
        day_link.click()
        
    def visible_check_dayli_visits_section(self, day_id:str) -> bool:
        day_id.replace('link', 'item')
        try:
            day_section = self.driver.find_element(By.ID, day_id)
            if day_section.is_displayed():
                return True
            else: return False
        except NoSuchElementException:
            return False
        
    def get_visit_form_visit_section(self, day_id: str) -> List[List]:
        day_id.replace('link', 'item')
        day_section = self.driver.find_element(By.ID, day_id)
        day_visits = day_section.find_elements(By.ID, 'availableVisit')
        result = []
        for visit in day_visits:
            visit_info = []
            visit_info.append(visit.get_attribute("data-visit-id"))
            for id in ['startTime', 'endTime', 'visitName', 'visitDate', 'doctor']:
                visit_info.append(visit.find_element(By.ID, id))
            try:
                assign_btn = visit.find_element(By.ID, 'assignBtn')
                visit_info.append(True)
            except NoSuchElementException:
                visit_info.append(False)
            result.append(visit_info)
        return result
    
    def click_on_assing_button_on_visit(self, visit_id: str) -> None:
        visit = self.driver.find_elements(By.CSS_SELECTOR, f'div[data-visit-id="{visit_id}"]')
        self.driver.execute_script("arguments[0].scrollIntoView();", visit)
        assign_btn = visit.find_element(By.ID, 'assignBtn')
        assign_btn.click()

    
    def visible_check_assign_confirmation(self, visit_id: str) -> bool:
        visit_id.replace('visit', 'confirm')
        try:
            confirmation = self.driver.find_elements(By.CSS_SELECTOR, f'div[data-visit-id="confirm{visit_id}"]')
            return True
        except NoSuchElementException:
            return False
        
    def get_text_on_confirmation(self, visit_id: str) -> str:
        visit_id.replace('visit', 'confirm')
        confirmation = self.driver.find_elements(By.CSS_SELECTOR, f'div[data-visit-id="confirm{visit_id}"]')
        confirmation_text = confirmation.find_element(By.CLASS_NAME, 'modal-body').text
        return confirmation_text
    
    def click_on_close_confirmation_button(self) -> None:
        button = self.driver.find_element(By.CSS_SELECTOR, 'button[data-bs-dismiss="modal"]')
        button.click()
        
    def click_on_assign_confirmatino_button(self) -> None:
        button = self.driver.find_element(By.NAME, 'confirmBtn')
        button.clisk()
        
    def visible_check_upcoming_visits(self) -> bool:
        try:
            upcoming_visits = self.driver.find_element(By.CSS_SELECTOR, '.upcoming-visit')
            return True
        except NoSuchElementException:
            return False
        
    def visible_check_past_visits(self) -> bool:
        try:
            past_visits = self.driver.find_element(By.CSS_SELECTOR, '.past-visit')
            return True
        except NoSuchElementException:
            return False
        
    def get_upcoming_visits(self) -> List[List]:
        past_visits = self.driver.find_element(By.CSS_SELECTOR, '.upcoming-visit')
        result = []
        for visit in past_visits:
            visit_info = []
            visit_info.append(visit.get_attribute("upcoming-visit-id"))
            for id in ['uVisitName', 'uVisitDate', 'uVisitTime', 'uDoctor']:
                visit_info.append(visit.find_element(By.ID, id))
            try:
                datail_btn = visit.find_element(By.ID, 'uDetailBtn')
                visit_info.append(True)
            except NoSuchElementException:
                visit_info.append(False)
            result.append(visit_info)
        return result
    
    def get_past_visits(self) -> List[List]:
        past_visits = self.driver.find_element(By.CSS_SELECTOR, '.past-visit')
        result = []
        for visit in past_visits:
            visit_info = []
            visit_info.append(visit.get_attribute("past-visit-id"))
            for id in ['pVisitName', 'pVisitDate', 'pVisitTime', 'pDoctor']:
                visit_info.append(visit.find_element(By.ID, id))
            try:
                datail_btn = visit.find_element(By.ID, 'pDetailBtn')
                visit_info.append(True)
            except NoSuchElementException:
                visit_info.append(False)
            result.append(visit_info)
        return result
        
    def click_on_detail_in_upcoming_visit(self, visit_id: str) -> None:
        upcoming_visit_card = self.driver.find_element(By.XPATH, f'//*[@upcoming-visit-id="{visit_id}"]')
        self.driver.execute_script("arguments[0].scrollIntoView();", upcoming_visit_card)
        detail_btn = upcoming_visit_card.find_element(By.ID, 'uDetailBtn')
        detail_btn.click()
        
    def click_on_detail_in_past_visit(self, visit_id: str) -> None:
        past_visit_card = self.driver.find_element(By.XPATH, f'//*[@past-visit-id="{visit_id}"]')
        self.driver.execute_script("arguments[0].scrollIntoView();", past_visit_card)
        detail_btn = past_visit_card.find_element(By.ID, 'pDetailBtn')
        detail_btn.click()
        
                
        
    