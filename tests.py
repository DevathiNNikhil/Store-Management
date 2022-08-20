from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class LoginFormTest(LiveServerTestCase):

	def testform(self):
		driver = webdriver.Chrome()

		driver.get('http://127.0.0.1:8000/')


		user_name = driver.find_element_by_name('username')
		user_password = driver.find_element_by_name('password')

		submit = driver.find_element_by_name('log')

		user_name.send_keys('Nikhil')
		user_password.send_keys('nithin1234')

		submit.send_keys(Keys.RETURN)

		assert 'add' in driver.page_source
		