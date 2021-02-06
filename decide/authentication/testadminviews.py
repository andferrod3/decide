from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from base.tests import BaseTestCase


class AdminTestCase(StaticLiveServerTestCase):

   
    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.FirefoxOptions()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

        super().setUp()            
    
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()
        

    def test_egc(self):
        driver = self.driver
        self.driver.get(f'{self.live_server_url}/admin/')
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("admin")
        driver.find_element_by_id("id_password").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("admin123")
        driver.find_element_by_xpath("//input[@value='Log in']").click()
        self.assertEqual("WELCOME, ADMIN.", driver.find_element_by_xpath("//div[@id='user-tools']/strong").text)
    

    def test_simpleWrongLogin(self):

        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element_by_id('id_username').send_keys("WRONG")
        self.driver.find_element_by_id('id_password').send_keys("WRONG")       
        self.driver.find_element_by_id('login-form').submit()

        #In case a incorrect login, a div with class 'errornote' is shown in red!
        self.assertTrue(len(self.driver.find_elements_by_class_name('errornote'))==1)
        
        
        
