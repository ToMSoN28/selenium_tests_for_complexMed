from selenium import webdriver
from pages.page import Page
from selenium.webdriver.common.by import By


class LoginPage(Page):
    
    def __init__(self, driver: webdriver, base_url: str) -> None:
        self.driver = driver
        self.base_url = base_url
        self.endpoint = 'login/'
        pass
    
    # locators = {
    #     'user_name': ('ID', 'typeLoginX'),
    #     'password': ('ID', 'typePasswordX'),
    #     'login_btn': ('ID', 'loginBtn')
    # }
    
    def open_login_page(self) -> None:
        self.driver.get(f'{self.base_url}{self.endpoint}')
        pass
    
    def enter_user_login(self, user_login: str) -> None:
        # self.user_name.send_text(user_login)
        user_input = self.driver.find_element(By.ID, "typeLoginX")
        user_input.clear()
        user_input.send_keys(user_login)
        pass
    
    def enter_password(self, user_password: str) -> None:
        password_input = self.driver.find_element(By.ID, "typePasswordX")
        password_input.clear()
        password_input.send_keys(user_password)
        pass
    
    def click_on_login_button(self) -> None:
        login_button = self.driver.find_element(By.ID, "loginBtn")
        login_button.click()
        pass
    