from django.shortcuts import render, redirect
from django.http import HttpResponse

from spend.models import Expense

# Create your views here.
def home_page(request):
	if request.method == 'POST':
		Expense.objects.create(location = request.POST['expense_where'])
		return redirect('/')
	
	expenses = Expense.objects.all()
	return render(request, 'home.html', { 'expenses': expenses })