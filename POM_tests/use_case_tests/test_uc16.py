import pytest
from typing import Literal
from pages.create_account_page import CreateAccountPage
from pages.worker_list_page import WorkerListPage


class TestUC16:
    
    def login(self, login, setup_method, user_credentials, user) -> CreateAccountPage:
        user_l, user_p = user_credentials[user]
        login(user_l, user_p)
        driver, base_url = setup_method
        create_account_page = CreateAccountPage(driver, base_url)
        return create_account_page
    
    def fill_and_send_form(self, create_account_page: CreateAccountPage, username: str, first_name: str, last_name: str, email: str, function: Literal['Receptionist', 'Doctor'], password: str, password_again: str) -> None:
        create_account_page.enter_username(username)
        create_account_page.enter_first_name(first_name)
        create_account_page.enter_last_name(last_name)
        create_account_page.enter_emial(email)
        create_account_page.select_function(function)
        create_account_page.enter_password(password)
        create_account_page.enter_password_again(password_again)
        create_account_page.click_on_register_button()
    
    @pytest.mark.parametrize("user, visible", [
        ("manager", True),
        ("doctor", False),
        ("receptionist", False)
    ])
    def test_go_to_create_account(self, login, setup_method, get_current_url, user_credentials, user, visible):
        create_account_page = self.login(login, setup_method, user_credentials, user)
        assert create_account_page.visible_check_create_account() == visible
        if visible:
            create_account_page.click_on_create_acount()
            assert get_current_url(create_account_page.driver) == '/crate-account/'
            
    def test_create_allredy_existing_username(self, login, setup_method, user_credentials):
        user = 'manager'
        username = 'doctor1'
        first_name = 'Tom'
        last_name = 'Kow'
        emial = 'tom@kow.pl'
        function = 'Doctor'
        password = 'qwerty12'
        password_again = 'qwerty12'
        create_account_page = self.login(login, setup_method, user_credentials, user)
        create_account_page.click_on_create_acount()
        self.fill_and_send_form(create_account_page, username, first_name, last_name, emial, function, password, password_again)
        error_msg = create_account_page.get_error_messege()
        assert error_msg == f'Username: {username} is already used. Create account again.'
        
    def test_create_account_with_diffrent_passwords(self, login, setup_method, user_credentials):
        user = 'manager'
        username = 'tomkow'
        first_name = 'Tom'
        last_name = 'Kow'
        emial = 'tom@kow.pl'
        function = 'Receptionist'
        password = 'qwerty12'
        password_again = '12qwerty'
        create_account_page = self.login(login, setup_method, user_credentials, user)
        create_account_page.click_on_create_acount()
        self.fill_and_send_form(create_account_page, username, first_name, last_name, emial, function, password, password_again)
        error_msg = create_account_page.get_error_messege()
        assert error_msg == f'Passwords are not the same. Create account again.'
        
    def test_create_receptionist(self, login, setup_method, user_credentials):
        pass
    
    def test_create_doctor(self, login, setup_method, user_credentials):
        pass