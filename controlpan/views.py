from django.shortcuts import render, redirect
from blogpost.models import *
from django.contrib.auth import login, authenticate, logout #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from .forms import AccountAuthenticationForm
from numerize import numerize 

# Create your views here.
def index(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.get(user=user)
        posts = Post.objects.filter(profile=profile, isPublished=True)
        profilepost = numerize.numerize(profile.total_posts)
        publishedpost = numerize.numerize(profile.published_post)
        draftpost = numerize.numerize(profile.draft_posts)
        profilecomment = numerize.numerize(profile.total_comments)
        profileimpressions = numerize.numerize(profile.totalpost_impressions)
        context['user'] = user
        context['posts'] = posts
        context['profile'] = profile
        context['profilepost'] = profilepost
        context['publishedpost'] = publishedpost
        context['draftpost'] = draftpost
        context['profilecomment'] = profilecomment
        context['profileimpressions'] = profileimpressions
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
			
            form.save(request)
            return redirect("index")

        else:
            context['login_form'] = form

    
    
    
    return render(request, "index.html", context)


def logout_view(request):
	logout(request)
	return redirect("index")

def editbio(request):
    user = request.user
    context = {
        "user": user
    }

    if user.is_authenticated:
        profile = Profile.objects.get(user=user)
        if request.POST:
            profile.bio = request.POST.get("bio")
            profile.save()
            return redirect("index")
    else:
        return redirect("index")
    
    return render(request, "editbio.html", context)
        