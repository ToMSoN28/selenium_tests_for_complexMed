import time
import pytest
from pages.worker_list_page import WorkerListPage

class TestWorkersListPage:
    
    def test_all_warkers_on_page(self, login, setup_method, user_credentials):
        user = 'manager'
        expected_tebale = [
            ['Adam Wiśniewski', 'doctor1', False, True, False],
            ['Ewa Szymańska', 'doctor2', False, True, False],
            ['Marek Zieliński', 'receptionist1', False, False, True],
            ['Magdalena Nowak', 'manager1', True, False, True]
        ]
        user_l, user_p = user_credentials[user]
        login(user_l, user_p)
        driver, base_url = setup_method
        worker_list_page = WorkerListPage(driver, base_url)
        worker_list_page.click_on_worker_list()
        worker_list = worker_list_page.get_workers_list()
        for worker in worker_list:
            assert worker in expected_tebale
        
        