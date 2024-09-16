import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver

class NavbarPage:
    
    def __init__(self, driver: webdriver) -> None:
        self.driver = driver
        pass
    
    def visible_check_daily_visits(self) -> bool:
        try:
            link = self.driver.find_element(By.ID, "DailyVisits")
            return link.is_displayed()
        except NoSuchElementException:
            return False
    
    def click_on_daily_visits(self) -> None:
        link = self.driver.find_element(By.ID, "DailyVisits")
        link.click()
    
    def visible_check_patient_registration(self) -> bool:
        try:
            link = self.driver.find_element(By.ID, "PatientRegistration")
            return link.is_displayed()
        except NoSuchElementException:
            return False
    
    def click_on_patient_registration(self) -> None:
        link = self.driver.find_element(By.ID, "PatientRegistration")
        link.click()
    
    def visible_check_search_patient(self) -> bool:
        try:
            link = self.driver.find_element(By.ID, "SearchPatient")
            return link.is_displayed()
        except NoSuchElementException:
            return False
    
    def click_on_search_patient(self) -> None:
        link = self.driver.find_element(By.ID, "SearchPatient")
        link.click()
    
    def visible_check_edit_schedule(self) -> bool:
        try:
            link = self.driver.find_element(By.ID, "EditSchedule")
            return link.is_displayed()
        except NoSuchElementException:
            return False
    
    def click_on_edit_schedule(self) -> None:
        link = self.driver.find_element(By.ID, "EditSchedule")
        link.click()
    
    def visible_check_worker_list(self) -> bool:
        try:
            link = self.driver.find_element(By.ID, "WorkerList")
            return link.is_displayed()
        except NoSuchElementException:
            return False
    
    def click_on_worker_list(self) -> None:
        link = self.driver.find_element(By.ID, "WorkerList")
        link.click()
    
    def visible_check_create_account(self) -> bool:
        try:
            link = self.driver.find_element(By.ID, "CreateAccount")
            return link.is_displayed()
        except NoSuchElementException:
            return False
    
    def click_on_create_acount(self) -> None:
        link = self.driver.find_element(By.ID, "CreateAccount")
        link.click()
    
    def visible_check_person_menu_button(self) -> bool:
        try:
            button = self.driver.find_element(By.ID, "navbarDropdown")
            button.click()
            # time.sleep(0.5)
            change_padssword_link = self.driver.find_element(By.ID, "NewPassword")
            logout_link = self.driver.find_element(By.ID, "Logout")
            result = button.is_displayed() and change_padssword_link.is_displayed() and logout_link.is_displayed()
            button.click()
            return result
        except NoSuchElementException:
            return False
    
    def click_on_person_menu_button(self) -> None:
        button = self.driver.find_element(By.ID, "navbarDropdown")
        button.click()
        
    def is_open_preson_menu_button(self) -> bool:
        button = self.driver.find_element(By.ID, "navbarDropdown")
        return 'show' in button.get_attribute('class')
    
    def click_on_new_password(self) -> None:
        change_padssword_link = self.driver.find_element(By.ID, "NewPassword")
        change_padssword_link.click()
        
    def click_on_logout(self) -> None:
        logout_link = self.driver.find_element(By.ID, "Logout")
        logout_link.click()
    
    
    