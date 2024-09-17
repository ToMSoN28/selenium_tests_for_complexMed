from selenium import webdriver
from pages.navbar_page import NavbarPage
from selenium.webdriver.common.by import By

class ChangePasswordPage(NavbarPage):
    
    def __init__(self, driver: webdriver, base_url: str) -> None:
        super().__init__(driver)
        self.driver = driver
        self.base_url = base_url
        self.endpoint = 'change-password/'
        
    def open_change_password_page(self) -> None:
        self.driver.get(f'{self.base_url}{self.endpoint}')
        pass
    
    def enter_old_password(self, old_password: str) -> None:
        old_password_input = self.driver.find_element(By.ID, 'inputOldPassword')
        old_password_input.clear()
        old_password_input.send_keys(old_password)
        
    def enter_new_password(self, new_password: str) -> None:
        new_password_input = self.driver.find_element(By.ID, 'inputPassword')
        new_password_input.clear()
        new_password_input.send_keys(new_password)
        
    def enter_confirm_password(self, confirm_password: str) -> None:
        confirm_password_input = self.driver.find_element(By.ID, 'inputPasswordAgain')
        confirm_password_input.clear()
        confirm_password_input.send_keys(confirm_password)
        
    def click_on_change_button(self) -> None:
        button = self.driver.find_element(By.ID, 'changeButton')
        button.click()
        
    def check_error_message(self):
        error_msg = self.driver.find_element(By.ID, 'errorMsg')
        return error_msg.text