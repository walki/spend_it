from django.shortcuts import render, redirect
from django.http import HttpResponse

from spend.models import Expense

# Create your views here.
def home_page(request):
	return render(request, 'home.html')

def view_list(request):
	expenses = Expense.objects.all()
	return render(request, 'expense.html', { 'expenses': expenses })

def new_expense_list(request):
	Expense.objects.create(location = request.POST['expense_where'],
							date = request.POST.get('expense_date',''))
	return redirect('/spends/the-only-list/')
