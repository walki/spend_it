from django.shortcuts import render, redirect
from django.http import HttpResponse

from spend.models import Expense, ExpenseList

# Create your views here.
def home_page(request):
	return render(request, 'home.html')

def view_list(request):
	expenses = Expense.objects.all()
	return render(request, 'expense.html', { 'expenses': expenses })

def new_expense_list(request):
	exp_list = ExpenseList.objects.create()
	Expense.objects.create(location = request.POST['expense_where'],
							date = request.POST.get('expense_date',''),
							expense_list = exp_list)
	return redirect('/spends/the-only-list/')
