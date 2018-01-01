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
		self.client.post('/', data={'expense_where': 'A new expense'})

		self.assertEqual(Expense.objects.count(), 1)
		new_expense = Expense.objects.first()
		self.assertEqual(new_expense.location, "A new expense")

	def test_can_save_a_POST_request_with_date(self):
		self.client.post('/', data={'expense_where': 'A new expense', 'expense_date': '12-31-2001'})

		self.assertEqual(Expense.objects.count(), 1)
		new_expense = Expense.objects.first()
		self.assertEqual(new_expense.date, '12-31-2001')


	def test_redirects_after_a_POST_request(self):
		response = self.client.post('/', data={'expense_where': 'A new expense'})

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/spends/the-only-list/')

	def test_only_saves_expenses_when_necessary(self):
		self.client.get('/')
		self.assertEqual(Expense.objects.count(), 0)




class ExpenseModelTest(TestCase):

	def test_saving_and_retreiving_expense_locations(self):
		first_expense = Expense()
		first_expense.location = 'The first (ever) expense!'
		first_expense.save()

		second_expense = Expense()
		second_expense.location = 'The Second'
		second_expense.save()

		saved_expenses = Expense.objects.all()
		self.assertEqual(saved_expenses.count(), 2)

		first_saved_expense = saved_expenses[0]
		second_saved_expense = saved_expenses[1]
		self.assertEqual(first_saved_expense.location, 'The first (ever) expense!')
		self.assertEqual(second_saved_expense.location, 'The Second')

	def test_saving_and_retrieving_expense_with_location_and_date(self):
		expense = Expense()
		expense.location = "The Location"
		expense.date = "1-2-2001"
		expense.save()

		saved_expenses = Expense.objects.all()
		self.assertEqual(saved_expenses.count(), 1)
		saved_expense = saved_expenses.first()

		self.assertEqual(saved_expense.location, "The Location")
		self.assertEqual(saved_expense.date, "1-2-2001")


class ListViewTest(TestCase):

	def test_uses_expense_template(self):
		response = self.client.get('/spends/the-only-list/')
		self.assertTemplateUsed(response, 'expense.html')

	def test_displays_all_items(self):
		Expense.objects.create(location='Loc 1')
		Expense.objects.create(location='Loc 2')

		response = self.client.get('/spends/the-only-list/')

		self.assertContains(response, 'Loc 1')
		self.assertContains(response, 'Loc 2')

	def test_displays_expenses_with_dates(self):
		Expense.objects.create(location='exp 1', date='1-10-2018')

		response = self.client.get('/spends/the-only-list/')

		self.assertIn('exp 1', response.content.decode())
		self.assertIn('1-10-2018', response.content.decode())
