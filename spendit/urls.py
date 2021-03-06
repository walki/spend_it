"""spendit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from spend import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^spends/new$', views.new_expense_list, name='new_expense_list'),
	url(r'^spends/(\d+)/$', views.view_list, name='view_list'),
    url(r'^spends/(\d+)/add_expense$', views.add_expense, name='add_expense'),
]
