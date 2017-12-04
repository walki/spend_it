from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
	
	def tearDown(self):
		self.browser.quit()
		
		
	def wait_for_row_in_expense_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_expense_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)
		
	def test_can_start_adding_expenses_and_retrieve_later(self):
		# Andrea wants to help with the budget using a cool new expesne tracking software
		# She goes to its homepage 
		self.browser.get(self.live_server_url)

		# She notices that the page title and header mention Spend It!
		self.assertIn('Spend It!', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Spend It!', header_text)
		
		# She is invited to add an expense right away
		inputbox = self.browser.find_element_by_id('id_new_expense')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter an expense'
		)

		# She is invited to add a date for the expense
		dateinputbox = self.browser.find_element_by_id('id_new_date')
		self.assertEqual(
			dateinputbox.get_attribute('placeholder'),
			'Enter a date'
		)
		
		# She adds "Heinens" into a text box, as it is here favorite grocery store
		inputbox.send_keys('Heinens')

		# She adds a '1-1-2018' for the date
		dateinputbox.send_keys('1-1-2018')
		
		# When she hits enter the page updates, and now the page lists
		# "1/1/2018 Heniens 10.00" as an item that has been added as an expense
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_expense_table('1: 1-1-2018 Heinens 10.00')
		
		# There is still an a text box inviting to add another expense.
		# She enters "Target" as she frequently shops there also.
		inputbox = self.browser.find_element_by_id('id_new_expense')
		inputbox.send_keys('Target')
		dateinputbox = self.browser.find_element_by_id('id_new_date')
		dateinputbox.send_keys('2-1-2018')
		inputbox.send_keys(Keys.ENTER)

		# The page updates again, and both expenses are listed
		self.wait_for_row_in_expense_table('1: 1-1-2018 Heinens 10.00')
		self.wait_for_row_in_expense_table('2: 2-1-2018 Target 10.00')		
		
		# Andrea wonders whether the expenses are saved. She notices that in th first go through, expense are added per unique URL,
		# there is some text explaining that
		self.fail('Finish the test!')
		
		# She visits the URL and her expenses are still there

		# Satisfied, she leave
		