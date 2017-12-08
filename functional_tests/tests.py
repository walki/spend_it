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
		
	def test_can_start_adding_expenses_for_one_user(self):
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
		self.wait_for_row_in_expense_table('2: 2-1-2018 Target 10.00')		
		self.wait_for_row_in_expense_table('1: 1-1-2018 Heinens 10.00')
				
	
	def test_multiple_users_can_start_lists_at_differenty_urls(self):
		# Andrea starts a new expenses list
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_expense')
		inputbox.send_keys('Giant Eagle')
		dateinputbox = self.browser.find_element_by_id('id_new_date')
		dateinputbox.send_keys('12-12-2017')
		inputbox.send_keys(Keys.ENTER)

		self.wait_for_row_in_expense_table('1: 12-12-2017 Giant Eagle 10.00')
		
		# She notices that her list has a unique URL
		andrea_list_url = self.browser.current_url
		self.assertRegex(andrea_list_url, '/spends/.+')
		
		# Now another user comes along, Anna ...
		
		## We use a new browser session, no info from the cookies...
		self.browser.quit()
		self.browser = webdriver.Firefox()
		
		# Anna visits the home page, and there is no sign of Andrea's list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Giant Eagle', page_text)
		self.assertNotIn('Heinens', page_text)
		
		# Anna starts her own list of expenses
		inputbox = self.browser.find_element_by_id('id_new_expense')
		inputbox.send_keys('Jo Ann Fabrics')
		dateinputbox = self.browser.find_element_by_id('id_new_date')
		dateinputbox.send_keys('12-28-2017')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_expense_table('1: 12-28-2017 Jo Ann Fabrics 10.00')
		
		#Anna gets her own unique URL
		anna_list_url = self.browser.current_url
		self.assertRegex(anna_list_url, '/spends/.+')
		self.assertNotEqual(anna_list_url, andrea_list_url)
		
		# And there is still no trace of Andrea's items
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Giant Eagle', page_text)
		self.assertIn('Jo Ann Fabrics', page_text)
		
		# Satisfied, they both go back to sleep...
		