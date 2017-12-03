from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from spend.views import home_page
from spend.models import Expense

class HomePageTest(TestCase):
	
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)
	
	def test_uses_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')
		
	def test_can_save_a_POST_request(self):
		response = self.client.post('/', data={'item_expense_where': 'A new expense'})
		self.assertIn('A new expense', response.content.decode())
		self.assertTemplateUsed(response, 'home.html')
		

class ExpenseModelTest(TestCase):

	def test_saving_and_retreiving_expenses(self):
		first_expense = Expense()
		first_expense.text = 'The first (ever) expense!'
		first_expense.save()
		
		second_expense = Expense()
		second_expense.text = 'The Second'
		second_expense.save()
		
		saved_items = Expense.objects.all()
		self.assertEqual(saved_items.count(), 2)
		
		first_saved_expense = saved_items[0]
		second_saved_expense = saved_items[1]
		self.assertEqual(first_saved_expense.text, 'The first (ever) expense!')
		self.assertEqual(second_saved_expense.text, 'The Second')