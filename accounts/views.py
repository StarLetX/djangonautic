# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout

def signup_view(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			#log the user in
			user = form.save()
			login(request, user)
			return redirect('articles:list')
	else:
		form = UserCreationForm()
	return render(request, 'accounts/signup.html', {'form':form})


def login_view(request):
	if request.method == "POST":
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			#log in the user
			#we need to know who wants to login before we can log them in 
			#and we do that with the .get_user()
			user = form.get_user()
			login(request, user)
			if 'next' in request.POST:
				return redirect(request.POST.get('next'))
			else:
				return redirect('articles:list')
	else:
		form = AuthenticationForm()
	return render(request, 'accounts/login.html', { 'form':form })


def logout_view(request):
	if request.method == "POST":
		#the logout() doesn't take the user argument because it is the user that passed the post request 
		logout(request)
		return redirect('articles:list')
