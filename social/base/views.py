from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Twitter
from django.contrib import messages
from .form import TweetForm, SignUpForm, ProfilePicForms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

# Create your views here.

def home(request):
    tweets = []  # Initialize with an empty list
    form = TweetForm()
    if request.user.is_authenticated:
        tweets = Twitter.objects.all().order_by("-created_at")
        profiles = Profile.objects.all()
        form = TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                messages.success(request, "your tweet has been posted")
                return redirect('home')
            
    
    context = {'tweets':tweets, "form":form}
    return render(request, 'base/home.html', context)


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user = request.user)
        context={"profiles": profiles}
        return render(request, 'base/profile_list.html', context)
    else:
        messages.warning(request,'you must be logged in to visit profile')
        
        return redirect('home')
    
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(pk=pk)
        follower = profile.follow.all()
        following = profile.followed_by.all()
        show = profile.id != request.user.id
        
        tweet = Twitter.objects.filter(user = pk).order_by("-created_at")
        print(tweet)
        
        
        #follow logi
        if request.method == "POST":
            #current user id 
            current_user_profile = request.user.profile
            #get form data
            action = request.POST['follow']
            #decide to follor or unfolloe
            if action == "unfollow":
                current_user_profile.follow.remove(profile)
            elif action == "follow":
                current_user_profile.follow.add(profile)
            
            current_user_profile.save()
            
    
    context = {"profile":profile, 'follower':follower, 'following':following, "show":show, "tweet":tweet}
    return render(request, 'base/profile.html', context)

def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            
            profiles = Profile.objects.get(pk = pk)
            
            return render(request, 'base/followers.html', {"profiles":profiles})
        else:
            messages.warning(request, "thats not your profile")
            return redirect('home')
    else:
        messages.warning(request, 'you must be logged in')
        return redirect("home")
    
def following(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            
            profiles = Profile.objects.get(pk = pk)
            
            return render(request, 'base/following.html', {"profiles":profiles})
        else:
            messages.warning(request, "thats not your profile")
            return redirect('home')
    else:
        messages.warning(request, 'you must be logged in')
        return redirect("home")
    


    



def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            
            messages.success(request, "you have succesfully login")
            return redirect('home')
        else:
            messages.warning(request, 'there was an error in loggin in please try later')
            return redirect('login')  
        
    else:
        context= {}
        return render(request, 'base/login.html', context)


def logout_user(request):
    logout(request)
    
    
    messages.warning(request, "you are logged out of the app")
    
    return redirect('login')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email_name = form.cleaned_data['email']
            
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, 'you have succusfully register')
            return redirect('home')
    
    
    
    context = {'form': form}
    return render(request, 'base/register.html', context)


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        profile = Profile.objects.get(user__id = request.user.id)
        form = SignUpForm(request.POST or None,request.FILES or None, instance = current_user)
        profile_form = ProfilePicForms(request.POST or None, request.FILES or None, instance=profile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, 'your profile has been updated')
            return redirect('profile')
        
        
        
        context = {"form": form, "profile_form":profile_form}
        return render(request, 'base/update_user.html', context)
        
    
    else:
        messages.warning(request, "you must be logged in ")
        return redirect('login')
    
  

def tweet_like(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Twitter, pk=pk)
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user)
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            tweet.likes.add(request.user)
        # print(request.META.get("HTTP_REFERER"))
        return redirect(request.META.get("HTTP_REFERER"))
    
    else:
        messages.warning(request, "you must be logged in ")
        return redirect('login')
    
    
def tweet_share(request, pk):
    if request.user.is_authenticated: 
        tweet = get_object_or_404(Twitter, pk=pk)
        if tweet:
            return render(request, 'base/show_tweet.html', {"tweets":tweet})
            
            
        else:
            messages.warning(request, "that tweet doesnot exits ")
            return redirect('home')
            

def unfollow_user(request, pk):
    if request.user.is_authenticated:
        
        profile = Profile.objects.get(pk=pk)
        
        request.user.profile.follow.remove(profile)
        request.user.profile.save()
        
        messages.success(request, "unfollow success")
        return redirect(request.META.get("HTTP_REFERER"))
    
    messages.success(request, "you must be logged in")
    return redirect("home")



def follow_user(request, pk):
    
    if request.user.is_authenticated:
        profile = Profile.objects.get(pk=pk)
        
        request.user.profile.follow.add(profile)
        
        request.user.profile.save()
        
        return redirect(request.META.get("HTTP_REFERER"))
        
    
    
    
    return redirect('home')
        

def deletepost(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Twitter, pk=pk)
        if request.user.username == tweet.user.username:
            
            tweet.delete()
            
            messages.success(request, 'tweet delete success')
        
        else:
            messages.warning(request, "that's not your tweet")
        
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        
        messages.warning(request, "sorry you are not authenticated")
        return redirect('home')
    
    
def editpost(request, pk):
    if request.user.is_authenticated:
        tweets = get_object_or_404(Twitter, pk=pk)
        
        if request.user.username == tweets.user.username:
            form = TweetForm(request.POST or None, instance=tweets)
            if request.method == "POST":
                if form.is_valid():
                    tweets = form.save(commit=False)
                    tweets.user = request.user
                    tweets.save()
                    messages.success(request, "tweet updated success")
                    return redirect('home')
            
            else:
                return render(request, 'base/edit_tweet.html', {"form": form, "tweets":tweets})
        else:
            messages.warning(request, "that's not your tweet")
            return redirect(request.META.get("HTTP_REFERER"))
    
    else:
        
        messages.warning(request, "please login first")
        return redirect('login')
        
        
        
    
def search(request):
    
    if request.user.is_authenticated:
        if request.method == "POST":
            search = request.POST['search']
            
            tweets = Twitter.objects.filter(body__contains = search)
        
        
            return render(request, 'base/search.html',{ 'tweets': tweets, 'search':search})
        else:
            return render(request, 'base/search.html',{})
            
        
    
    else:
        return redirect('login')



def searchuser(request):
    if request.user.is_authenticated:
        
        if request.method == "POST":
            search = request.POST['search']
            
            profiles = User.objects.filter(username__contains = search)
            
            return render(request, 'base/searchuser.html', {"search":search, "profiles":profiles})
        else:
           
            return render(request, 'base/searchuser.html',{})
    
    else:
        messages.warning(request, "you are not logged in ")
        return redirect('login')