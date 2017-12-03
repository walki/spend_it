from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
	
	def tearDown(self):
		self.browser.quit()
		
	def test_can_start_adding_expenses_and_retrieve_later(self):
		# Andrea wants to help with the budget using a cool new expesne tracking software
		# She goes to its homepage 
		self.browser.get('http://localhost:8000')

		# She notices that the page title and header mention Spend It!
		self.assertIn('Spend It!', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Spend It!', header_text)
		self.fail('Finish the Test!')

		# She is invited to add an expense right away
		inputbox = self.browser.find_element_by_id('id_new_expense')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter an expense'
		)

		# She adds "Heinens" into a text box, as it is here favorite grocery store
		inputbox.send_keys('Heinens')

		# When she hits enter the page updates, and now the page lists
		# "1/1/2018 Heniens 10.00" as an item that has been added as an expense
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)
		
		table = self.browser.find_element_by_id('id_expense_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
			any(row.text == '1/1/2018 Heniens 10.00' for row in rows)
		)
		
		# There is still an a text box inviting to add another expense.
		# She enters "Target" as she frequently shops there also.
		self.fail('Finish the test!')

		# The page updates again, and both expenses are listed

		# Andrea wonders whether the expenses are saved. She notices that in th first go through, expense are added per unique URL,
		# there is some text explaining that

		# She visits the URL and her expenses are still there

		# Satisfied, she leave
		
if __name__ == '__main__':
	unittest.main(warnings='ignore')