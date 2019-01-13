from django.shortcuts import render
from django.http  import HttpResponse,Http404
import datetime as dt
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

# Create your views here.

# app view functions

# activate user function
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('thank you for confirming your email')
    else:
        return HttpResponse('the link is invalid!')

        
def index(request):
    date = dt.date.today()
    hoods = Neighbourhood.objects.all()
    return render(request, 'index.html',{"date":date, "hoods":hoods})


def profile(request):
    date = dt.date.today()
    current_user = request.user
    profile = Profile.objects.get(user=current_user.id)
    hoods = Neighbourhood.objects.all()
    return render(request, 'profile/profile.html', {"date": date, "profile":profile,"hoods":hoods})

def edit_profile(request):
    date = dt.date.today()
    current_user = request.user
    profile = Profile.objects.get(user=current_user.id)
    if request.method == 'POST':
        signup_form = EditForm(request.POST, request.FILES,instance=request.user.profile)
        if signup_form.is_valid():
            signup_form.save()
            return redirect('profile')
    else:
        signup_form =EditForm()

    return render(request, 'profile/edit_profile.html', {"date": date, "form":signup_form,"profile":profile})
@login_required(login_url='/accounts/login/')
def new_hood(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    if request.method == 'POST':
        form = HoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.user = current_user
            hood.profile = profile
            hood.save()
        return redirect('index')
    else:
        form = HoodForm()
    return render(request, 'new_hood.html', {"form": form})
def new_post(request,id):
    date = dt.date.today()
    hood=Neighbourhood.objects.get(id=id)
    posts = Post.objects.filter(neighbourhood=hood)
    comments = Comment.objects.filter(post=id).order_by('-pub_date')

    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.profile = profile
            post.neighbourhood = hood
            post.save()
            return redirect('index')
    else:
        form = PostForm()
        return render(request,'new_post.html',{"form":form,"posts":posts,"hood":hood,  "date":date, 'comments':comments})


@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'business' in request.GET and request.GET["business"]:
        search_term = request.GET.get("business")
        searched_businesses = Business.objects.filter(name=search_term)
        message = f"{search_term}"
        profiles=  Profile.objects.all( )

        return render(request, 'search.html',{"message":message,"business": searched_businesses,'profiles':profiles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})


def location(request):
    date = dt.date.today()
    return render(request, 'location.html',{"date":date})


def newcomment(request,id):
    current_user = request.user

    try:
        comments = Comment.objects.filter(post_id=id)
    except:
        comments = []
    brush= Post.objects.get(id=id)
    if request.method =="POST":
        form = NewCommentForm(request.POST,request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.postername = current_user
            comment.post = brush
            comment.save()
    else:
        form = NewCommentForm()

    return render(request, 'newcomment.html',{'brush':brush,"comments":comments,"form":form})



@login_required(login_url='/accounts/login/')
def hoods(request,id):
    current_user=request.user
    date = dt.date.today()
    post=Neighbourhood.objects.get(id=id)

    brushs = Post.objects.filter(neighbourhood=post)
    business = Business.objects.filter(neighbourhood=post)
    return render(request,'each_neighood.html',{"post":post,"date":date,"brushs":brushs, "business":business})


def post_business(request,id):
    date = dt.date.today()
    hood=Neighbourhood.objects.get(id=id)
    business = Business.objects.filter(neighbourhood=hood)
    form = BusinessForm()
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.profile = request.user.profile
            business.neighbourhood = hood
            business.save()
            return redirect('index')
    else:
        form = BusinessForm()
        return render(request,'new_business.html',{"form":form,"business":business,"hood":hood,  "date":date})