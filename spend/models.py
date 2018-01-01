from django.db import models

class ExpenseList(models.Model):
	pass

class Expense(models.Model):
	location = models.TextField(default = '')
	date = models.TextField(default = '')
	expense_list = models.ForeignKey(ExpenseList, default = None)
