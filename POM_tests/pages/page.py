from selenium import webdriver
from urllib.parse import urlparse

class Page:
    
    def __init__(self, driver: webdriver, base_url: str) -> None:
        self.driver = driver
        self.base_url = base_url
        
        pass
    
    logout_endpoint = 'logout/'
    
    def get_current_url(self) -> str:
        print(urlparse(self.driver.current_url).path)
        return urlparse(self.driver.current_url).path
    
    def logout(self) -> None:
        self.driver.get(f'{self.base_url}{self.logout_endpoint}')