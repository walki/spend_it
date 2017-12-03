from django.db import models

class Expense(models.Model):
	location = models.TextField(default = '')
	date = models.TextField(default= '')
