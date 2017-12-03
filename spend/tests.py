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
		self.client.post('/', data={'item_expense_where': 'A new expense'})
		
		self.assertEqual(Expense.objects.count(), 1)
		new_expense = Expense.objects.first()
		self.assertEqual(new_expense.text, "A new expense")

	def test_redirects_after_a_POST_request(self):
		response = self.client.post('/', data={'item_expense_where': 'A new expense'})
		
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/')
		
	def test_only_saves_items_when_necessary(self):
		self.client.get('/')
		self.assertEqual(Expense.objects.count(), 0)

	def test_displays_all_expenses(self):
		Expense.objects.create(text='exp 1')
		Expense.objects.create(text='exp 2')
		
		response = self.client.get('/')
		
		self.assertIn('exp 1', response.content.decode())
		self.assertIn('exp 2', response.content.decode())
		

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