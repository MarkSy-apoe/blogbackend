from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from blogpost.models import *
from django.contrib.auth import login, authenticate, logout #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from .forms import AccountAuthenticationForm, SignUpForm
from numerize import numerize 

# Create your views here.
def index(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.get(user=user)
        posts = Post.objects.filter(profile=profile, isPublished=True)[:20]
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
    
    return render(request, "edit_bio.html", context)

def createpost(request):
    user = request.user
    style = Tag.objects.get(tag="Style")
    relationship = Tag.objects.get(tag="Relationship")
    design = Tag.objects.get(tag="Design")
    food = Tag.objects.get(tag="Food")
    wellbeing = Tag.objects.get(tag="Wellbeing")
    context={
        "style": style,
        "relationship": relationship,
        "design": design,
        "food": food,
        "wellbeing": wellbeing,
    }

    if user.is_authenticated == False:
        return redirect("index")
    
    else:
        profile = Profile.objects.get(user=user)    
        if profile.is_editor == False:
            return redirect("index")
    
        if request.POST:
            tag = Tag.objects.get(tag=request.POST.get("tag"))
            newpost = Post(title=request.POST.get("title"), breif=request.POST.get("breif"), snippet=request.POST.get("snippet"), headimg=request.FILES.get("image"), tag=tag, profile=profile)
            newpost.save()
            profile.draft_posts = profile.draft_posts + 1
            profile.total_posts = profile.total_posts + 1
            profile.save()
            return redirect("draft-posts")
    
    return render(request, "create_post.html", context)

def draftedpost(request):
    user = request.user
    
    context ={}

    if user.is_authenticated == False:
        return redirect("index")
    else:
        profile = Profile.objects.get(user=user)
        posts = Post.objects.filter(profile=profile, isPublished=False).order_by("-timestamp")

        context["profile"] = profile
        context["posts"] = posts
    
        if profile.is_editor == False:
            return redirect("index")
    
    return render(request, "draftedpost.html", context)
    
def editpost(request, pk):
    user = request.user
    post = Post.objects.get(slug=pk)
    context = {
        "post": post,
    }

    sections = Section.objects.filter(blogpost=post)

    if sections:
        context["sections"] = sections

    
     

    if user.is_authenticated == False:
        return redirect("index") 
    else:
        profile = Profile.objects.get(user=user)
        context["profile"] = profile
        if post.profile == profile:
            if request.POST:
                newsection = Section(secimg=request.FILES.get("image"), body=request.POST.get("body"), blogpost=post)
                newsection.save()
                return HttpResponseRedirect(request.path_info) 
        else:
            return redirect("index") 
    
    return render(request, "editpost.html", context)


def publishpost(request, pk):
    user = request.user    
    post = Post.objects.get(slug=pk)
    context ={
        "user": user,
        "post": post,
    }

    if user.is_authenticated == False:
        return redirect("index")
    else:
        profile = Profile.objects.get(user=user)
        if post.profile == profile:
            post.isPublished = True
            post.save()
            profile.published_post = profile.published_post + 1
            profile.draft_posts = profile.draft_posts - 1
        else:
            return redirect("index")
    
    return render(request, "published.html", context)

def deletepost(request, pk):
    user = request.user
    
    post = Post.objects.get(slug=pk)
    context = {
        "post": post,
    }

    if user.is_authenticated == False:
        return redirect("index")
    else:
        profile = Profile.objects.get(user=user)    
        if post.profile == profile:
            if post.isPublished:
                post.delete()
                profile.total_posts = profile.total_posts - 1
                profile.published_post = profile.published_post - 1
            else:
                post.delete()
                profile.total_posts = profile.total_posts - 1
                profile.draft_posts = profile.draft_posts - 1
        else:
            return redirect("index")

    return render(request, "deleted.html", context)


def manageteam(request):
    user = request.user
    

    team = Profile.objects.all()

    context = {
        "user": user,
        "teams": team,
    }

    if user.is_authenticated == False:
        return redirect("index")
    else:
        profile = Profile.objects.get(user=user)
        context["profile"] = profile

    
    return render(request, "manageteam.html", context)

def editteamMember(request, pk):
    user = request.user
    
    member = Profile.objects.get(id=pk)

    context ={
        "user": user,
        "member": member,
    }

    if user.is_authenticated == False:
        return redirect("index")
    else:  
        profile = Profile.objects.get(user=user)  
        if profile.is_owner == False:
            return redirect("manage-team")
        
        if member.is_owner == True:
            return redirect("manage-team")
        
        if request.POST:
            if member.is_editor:
                member.is_editor = False
                member.save()
            else:
                member.is_editor = True
                member.save()

            return HttpResponseRedirect(request.path_info)

    return render(request, "editmember.html", context)

def deletemember(request, pk):
    user = request.user
    

    member = Profile.objects.get(id=pk)
    usergoing = get_object_or_404(User, id=member.user.id)

    if user.is_authenticated == False:
        return redirect("index")
    else: 
        profile = Profile.objects.get(user=user)   
        if profile.is_owner == False:
            return redirect("manageteam")
        
        if member.is_owner == True:
            return redirect("manageteam")
        else:        
            usergoing.delete()
    
    return render(request, "deletemember.html")

def addteammember(request):
    user = request.user
    
    context={}

    if user.is_authenticated == False:
        return redirect("index")
    else:
        profile = Profile.objects.get(user=user)
        if profile.is_owner == False:
            return redirect("manageteam")
        
        if request.POST:
            form = SignUpForm(request.POST)
            if form.is_valid():
                Profile.objects.create(fname="change", lname="name", bio="change bio", user=form.save())
                form.save()
                return redirect("manage-team")
            else:
                context['addmember'] = form
    
    return render(request, "addmember.html", context)

def editname(request):
    user = request.user
    context = {}

    if user.is_authenticated == False:
        return redirect("index")
    else:
        profile = Profile.objects.get(user=user)
        context["profile"] = profile
        if request.POST:
            fname = request.POST.get("fname")
            lname = request.POST.get("lname")
          
            profile.fname = fname
            profile.lname = lname
            profile.save()
            return redirect("index")
        
    return render(request, "editname.html", context)

def changepfp(request):
    user = request.user
    context = {}

    if user.is_authenticated == False:
        return redirect("index")
    else:
        profile = Profile.objects.get(user=user)
        context["profile"] = profile
        if request.POST:
            image = request.FILES.get("pfp")

            profile.displaypic = image
            profile.save()
            return redirect("index")
        
    return render(request, "changepfp.html", context)


def unpublish(request, pk):
    user = request.user    
    post = Post.objects.get(slug=pk)
    context ={
        "user": user,
        "post": post,
    }

    if user.is_authenticated == False:
        return redirect("index")
    else:
        profile = Profile.objects.get(user=user)
        if post.profile == profile:
            post.isPublished = False
            post.save()
        else:
            return redirect("index")
    
    return render(request, "unpublished.html", context)
