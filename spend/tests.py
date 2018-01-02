from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from spend.views import home_page
from spend.models import Expense, ExpenseList

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_uses_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')


class ListAndExpenseModelTest(TestCase):

	def test_saving_and_retreiving_expense_locations(self):
		expense_list = ExpenseList()
		expense_list.save()

		first_expense = Expense()
		first_expense.location = 'The first (ever) expense!'
		first_expense.expense_list = expense_list
		first_expense.save()

		second_expense = Expense()
		second_expense.location = 'The Second'
		second_expense.expense_list = expense_list
		second_expense.save()

		saved_expense_list = ExpenseList.objects.first()
		self.assertEqual(saved_expense_list, expense_list)

		saved_expenses = Expense.objects.all()
		self.assertEqual(saved_expenses.count(), 2)

		first_saved_expense = saved_expenses[0]
		second_saved_expense = saved_expenses[1]
		self.assertEqual(first_saved_expense.location, 'The first (ever) expense!')
		self.assertEqual(first_saved_expense.expense_list, expense_list)
		self.assertEqual(second_saved_expense.location, 'The Second')
		self.assertEqual(second_saved_expense.expense_list, expense_list)

	def test_saving_and_retrieving_expense_with_location_and_date(self):
		expense_list = ExpenseList()
		expense_list.save()

		expense = Expense()
		expense.location = "The Location"
		expense.date = "1-2-2001"
		expense.expense_list = expense_list
		expense.save()

		saved_expenses = Expense.objects.all()
		self.assertEqual(saved_expenses.count(), 1)
		saved_expense = saved_expenses.first()

		self.assertEqual(saved_expense.location, "The Location")
		self.assertEqual(saved_expense.date, "1-2-2001")
		self.assertEqual(saved_expense.expense_list, expense_list)


class ListViewTest(TestCase):

	def test_uses_expense_template(self):
		exp_list = ExpenseList.objects.create()
		response = self.client.get(f'/spends/{exp_list.id}/')
		self.assertTemplateUsed(response, 'expense.html')

	def test_displays_only_items_for_that_list(self):
		correct_exp_list = ExpenseList.objects.create()
		Expense.objects.create(location='Loc 1', expense_list = correct_exp_list )
		Expense.objects.create(location='Loc 2', expense_list = correct_exp_list )

		other_exp_list = ExpenseList.objects.create()
		Expense.objects.create(location='Other Loc 1', expense_list = other_exp_list )
		Expense.objects.create(location='Other Loc 2', expense_list = other_exp_list )

		response = self.client.get(f'/spends/{correct_exp_list.id}/')

		self.assertContains(response, 'Loc 1')
		self.assertContains(response, 'Loc 2')
		self.assertNotContains(response, 'Other Loc 1')
		self.assertNotContains(response, 'Other Loc 2')

	def test_displays_expenses_with_dates(self):
		exp_list = ExpenseList.objects.create()
		Expense.objects.create(location='exp 1', date='1-10-2018', expense_list = exp_list)

		response = self.client.get(f'/spends/{exp_list.id}/')

		self.assertIn('exp 1', response.content.decode())
		self.assertIn('1-10-2018', response.content.decode())

	def test_passes_correct_list_to_template(self):
		other_exp_list = ExpenseList.objects.create()
		correct_exp_list = ExpenseList.objects.create()
		response = self.client.get(f'/spends/{correct_exp_list.id}/')
		self.assertEqual(response.context['expense_list'], correct_exp_list)


class NewExpenseTest(TestCase):

	def test_can_save_a_POST_request(self):
		self.client.post('/spends/new', data={'expense_where': 'A new expense'})

		self.assertEqual(Expense.objects.count(), 1)
		new_expense = Expense.objects.first()
		self.assertEqual(new_expense.location, "A new expense")

	def test_can_save_a_POST_request_with_date(self):
		self.client.post('/spends/new', data={'expense_where': 'A new expense',
							'expense_date': '12-31-2001'})

		self.assertEqual(Expense.objects.count(), 1)
		new_expense = Expense.objects.first()
		self.assertEqual(new_expense.date, '12-31-2001')


	def test_redirects_after_a_POST_request(self):
		response = self.client.post('/spends/new', data={'expense_where': 'A new expense'})
		new_exp_list = ExpenseList.objects.first()
		self.assertRedirects(response, f'/spends/{new_exp_list.id}/')

	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_exp_list = ExpenseList.objects.create()
		correct_exp_list = ExpenseList.objects.create()

		self.client.post(
			f'/spends/{correct_exp_list.id}/add_expense',
			data={'expense_where':'new expense existing list',
					'expense_date':'1-1-2018'}
		)

		self.assertEqual(Expense.objects.count(), 1)
		new_exp = Expense.objects.first()
		self.assertEqual(new_exp.location, 'new expense existing list')
		self.assertEqual(new_exp.expense_list, correct_exp_list)

	def test_redirects_to_expense_list_view(self):
		other_exp_list = ExpenseList.objects.create()
		correct_exp_list = ExpenseList.objects.create()

		response = self.client.post(
			f'/spends/{correct_exp_list.id}/add_expense',
			data={'expense_where':'new expense existing list',
					'expense_date':'1-1-2018'}
		)

		self.assertRedirects(response, f'/spends/{correct_exp_list.id}/')
