from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import Article
from django.contrib.auth.decorators import login_required
from . import forms


def article_list(request):
	articles = Article.objects.all()

	return render(request, 'articles/article_list.html', {'articles':articles} )


def article_detail(request, slug):
	#this queries the database for the slug passed in the url i.e (?P<slug>[\w-]+)
	#it then makes that article available in this view so that it can be passed to the template
	article = Article.objects.get(slug=slug)
	#return HttpResponse(slug)
	return render(request, 'articles/article_detail.html', { 'article':article })


@login_required(login_url="/accounts/login/")
def article_create(request):
	if request.method == "POST":
		form = forms.CreateArticle(request.POST, request.FILES)
		if form.is_valid():
			#commit=False tells the app "Hey hold on don't save yet."
			instance = form.save(commit=False)
			#we are calling the instance of the form(post) and querying it for the user
			#the person that is making the post so that we can used him/her to populate the author field of our model
			instance.author = request.user
			#when we now assign the user/author to our database, we now save the blog.
			instance.save()
			return redirect('articles:list')
	else:
		form = forms.CreateArticle()
	return render(request, 'articles/article_create.html', {"form": form})