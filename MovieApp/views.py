from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect,get_object_or_404
from .forms import MovieForm, CustomUserForm
from .models import Movie, Review
from django.contrib.auth.decorators import login_required

def index(request):
    movie=Movie.objects.all()
    return render(request,'index.html',{'M':movie})

def detail(request,id):
    movie=Movie.objects.get(id=id)
    review=Review.objects.filter(movie=id)
    return render(request,"detail.html",{'R': review, 'M': movie})

@login_required(login_url='MovieApp:login')
def add_movie(request):
    if request.method == "POST":
        user = request.user
        name = request.POST.get('name', )
        desc = request.POST.get('desc', )
        year = request.POST.get('year', )
        img = request.FILES.get('img')
        movie=Movie(user= user,name=name,desc=desc,year=year,img=img)
        movie.save()
    return render(request,'add.html')

@login_required(login_url='MovieApp:login')
def Update(request,id):
    inst = get_object_or_404(Movie,id=id)
    N = request.user
    if request.method=="POST":
        FM2=MovieForm(request.POST, request.FILES, instance=inst)
        if inst.user == N:
            if FM2.is_valid():
                FM2.save()
                return redirect('/')
        else:
            FM2 = MovieForm(instance=inst)
            print(" No Permission ")
            messages.info(request, 'You are not authorized')
    else:
        FM2 = MovieForm(instance=inst)
    return render(request,'edit.html',{'FM2':FM2,'movie':inst})
@login_required(login_url='MovieApp:login')
def Delete(request,id):
    N = request.user
    if request.method == "POST":
        DE = Movie.objects.get(id=id)
        print(DE.user, N)
        if DE.user == N:
            DE.delete()
            return redirect('/')
        else:
            messages.info(request, 'You are not authorized to delete this movie')
    return render(request,'delete.html')

def register_page(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('MovieApp:login')
    else:
        form = CustomUserForm()
    return render(request, 'register.html', {'form': form})

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            UN = request.POST.get('username')
            PS = request.POST.get('password')
            user= authenticate(request, username=UN,password=PS)
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                messages.info(request,'User credentials does not exist')
    return render(request, 'login.html')
def logoutpage(request):
    logout(request)
    return redirect('MovieApp:login')
@login_required(login_url='MovieApp:login')
def review_page(request,id):
    DE = Movie.objects.get(id=id)
    if request.method == "POST":
        U = request.user
        caption = request.POST.get('caption', )
        review = request.POST.get('review', )
        movie = DE.name
        RE = Review(user=U, caption=caption, review=review, movie=Movie.objects.get(name=movie))
        au=Review.objects.filter(movie=id).filter(user=U)
        if au.exists():
            messages.info(request, 'You have already submitted a Review')
        else:
            RE.save()
            return redirect('/')
    return render(request, 'reviewpage.html')

@login_required(login_url='MovieApp:login')
def re_delete(request,id):
    N = request.user
    if request.method == "POST":
        DE = Review.objects.get(id=id)
        print(DE.user,N)
        if DE.user == N:
            DE.delete()
            return redirect('/')
        else:
            messages.info(request, 'You are not authorized to delete this movie')
    return render(request,'re_delete.html')