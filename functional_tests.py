from selenium import webdriver
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
		self.fail('Finish the Test!')

		# She is invited to add an expense right away

		# She adds "Heinens" into a text box, as it is here favorite grocery store

		# When she hits enter the page updates, and now the page lists
		# "1/1/2018 Heniens 10.00" as an item that has been added as an expense

		# There is still an a text box inviting to add another expense.
		# She enters "Target" as she frequently shops there also.

		# The page updates again, and both expenses are listed

		# Andrea wonders whether the expenses are saved. She notices that in th first go through, expense are added per unique URL,
		# there is some text explaining that

		# She visits the URL and her expenses are still there

		# Satisfied, she leave
		
if __name__ == '__main__':
	unittest.main(warnings='ignore')