from django.db import models

class Expense(models.Model):
	text = models.TextField(default = '')
