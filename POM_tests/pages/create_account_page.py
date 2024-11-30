from selenium import webdriver
from selenium.webdriver.support.ui import Select
from pages.navbar_page import NavbarPage
from selenium.webdriver.common.by import By


class CreateAccountPage(NavbarPage):
    
    def __init__(self, driver: webdriver, base_url: str) -> None:
        # super().__init__(driver, base_url)
        self.driver = driver
        self.base_url = base_url
        self.endpoint = 'crate-account/'
        
    def enter_username(self, username: str) -> None:
        username_input = self.driver.find_element(By.ID, 'inputUsername')
        username_input.clear()
        username_input.send_keys(username)

    def enter_first_name(self, first_name: str) -> None:
        first_name_input = self.driver.find_element(By.ID, 'inputFirstName')
        first_name_input.clear()
        first_name_input.send_keys(first_name)
        
    def enter_last_name(self, last_name: str) -> None:
        last_name_input = self.driver.find_element(By.ID, 'inputLastName')
        last_name_input.clear()
        last_name_input.send_keys(last_name)
        
    def enter_emial(self, email: str) -> None:
        email_input = self.driver.find_element(By.ID, 'inputEmail')
        email_input.clear()
        email_input.send_keys(email)
        
    def get_function_option(self) -> Select.options:
        finction_dropdown = Select(self.driver.find_element(By.ID, 'selectFunction'))
        return finction_dropdown.options
    
    def select_function(self, function: str) -> None:
        function_dropdown = Select(self.driver.find_element(By.ID, 'selectFunction'))
        function_dropdown.select_by_visible_text(function)
        
    def enter_password(self, password: str) -> None:
        password_input = self.driver.find_element(By.ID, 'inputPassword')
        password_input.clear()
        password_input.send_keys(password)
        
    def enter_password_again(self, password: str) -> None:
        password_input = self.driver.find_element(By.ID, 'inputPasswordAgain')
        password_input.clear()
        password_input.send_keys(password)
        
    def click_on_register_button(self) -> None:
        button = self.driver.find_element(By.ID, 'register')
        button.click()
        
    def get_error_messege(self) -> str:
        return self.driver.find_element(By.ID, 'error').text
        
        
        