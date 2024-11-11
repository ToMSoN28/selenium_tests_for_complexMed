import pytest
from typing import List
from pages.worker_list_page import WorkerListPage


class TestWorkersListPage:
    
    workers_info = [
        {"first_name": "Adam", "last_name": "Wiśniewski", "username": "doctor1", "is_manager": False, "is_doctor": True, "is_receptionist": False},
        {"first_name": "Ewa", "last_name": "Szymańska", "username": "doctor2", "is_manager": False, "is_doctor": True, "is_receptionist": False},
        {"first_name": "Magdalena", "last_name": "Nowak", "username": "manager1", "is_manager": True, "is_doctor": False, "is_receptionist": True},
        {"first_name": "Marek", "last_name": "Zieliński", "username": "receptionist1", "is_manager": False, "is_doctor": False, "is_receptionist": True}
    ]
    
    def convert_workers_into_list(self, list: List[int]) -> List[List]:
        result = []
        for i, worker in enumerate(self.workers_info):
            if i in list:
                full_name = f"{worker['first_name']} {worker['last_name']}"
                result.append([full_name, worker['username'], worker['is_manager'], worker['is_doctor'], worker['is_receptionist']])
        return result
    
    def login(self, login, setup_method, user_credentials, user):
        user_l, user_p = user_credentials[user]
        login(user_l, user_p)
        driver, base_url = setup_method
        worker_list_page = WorkerListPage(driver, base_url)
        return worker_list_page
    
    @pytest.mark.parametrize("user, visible", [
        ("manager", True),
        ("doctor", False),
        ("receptionist", False)
    ])
    def test_go_to_worker_list(self, login, setup_method, get_current_url, user_credentials, user, visible):
        worker_list_page = self.login(login, setup_method, user_credentials, user)
        assert worker_list_page.visible_check_worker_list() == visible
        if visible:
            worker_list_page.click_on_worker_list()
            assert get_current_url(worker_list_page.driver) == '/workers-list/'
    
    def test_all_warkers_on_page(self, login, setup_method, user_credentials):
        user = 'manager'
        worker_list_page = self.login(login, setup_method, user_credentials, user)
        worker_list_page.click_on_worker_list()
        worker_list = worker_list_page.get_workers_list()
        expected_tebale = self.convert_workers_into_list([0,1,2,3])
        assert worker_list == expected_tebale
            
    @pytest.mark.parametrize("first_name, last_name, username", [
        ("", "", ""),
        ("da", "", ""),
        ("", "ski", ""),
        ("", "", "1"),
        ("da", "ak", ""),
        ("a", "", "doc"),
        ("", "ń", "2"),
        ("a", "e", "ce")
    ])       
    def test_search_workser(self, login, setup_method, user_credentials, first_name, last_name, username):
        user = 'manager'
        worker_list_page = self.login(login, setup_method, user_credentials, user)
        worker_list = worker_list_page.get_workers_list()
        worker_list_page.click_on_worker_list()
        worker_list_page.enter_first_name_in_worker_sherch(first_name)
        worker_list_page.enter_last_name_in_worker_sherch(last_name)
        worker_list_page.enter_username_in_worker_sherch(username)
        worker_list_page.click_on_search_button()
        worker_list = worker_list_page.get_workers_list()
        expected_table = []
        for i, worker in enumerate(self.workers_info):
            if first_name in worker['first_name'] and last_name in worker['last_name'] and username in worker['username']:
                expected_table.append(i)
        expected_table = self.convert_workers_into_list(expected_table)
        assert worker_list == expected_table
        
        
        
        