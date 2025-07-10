from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MovieForm, CustomUserForm
from .models import Movie, Review, Category
from django.contrib.auth.decorators import login_required


def index(request):
    movie = Movie.objects.all()
    return render(request, 'index.html', {'M': movie})


def allProdCat(request, c_slug=None):
    c_page = None
    movie = None
    if c_slug != None:
        c_page = get_object_or_404(Category, slug=c_slug)
        movie = Movie.objects.all().filter(category=c_page)
    else:
        movie = Movie.objects.all()
    return render(request, 'category.html', {'category': c_page, 'M': movie})


def detail(request, id):
    movie = Movie.objects.get(id=id)
    review = Review.objects.filter(movie=id)
    return render(request, "detail.html", {'R': review, 'M': movie})


@login_required(login_url='MovieApp:login')
def add_movie(request):
    p_category = Category.objects.all()
    if request.method == "POST":
        user = request.user
        name = request.POST.get('name', )
        category = Category.objects.get(id=request.POST['category'])
        desc = request.POST.get('desc', )
        year = request.POST.get('year', )
        img = request.FILES.get('img')
        movie = Movie(user=user, name=name, category=category, desc=desc, year=year, img=img)
        movie.save()
        return redirect('/')
    return render(request, 'add.html', {"p_category": p_category})


@login_required(login_url='MovieApp:login')
def Update(request, id):
    inst = get_object_or_404(Movie, id=id)
    N = request.user
    if request.method == "POST":
        FM2 = MovieForm(request.POST, request.FILES, instance=inst)
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
    return render(request, 'edit.html', {'FM2': FM2, 'movie': inst})


@login_required(login_url='MovieApp:login')
def Delete(request, id):
    N = request.user
    if request.method == "POST":
        DE = Movie.objects.get(id=id)
        print(DE.user, N)
        if DE.user == N:
            DE.delete()
            return redirect('/')
        else:
            messages.info(request, 'You are not authorized to delete this movie')
    return render(request, 'delete.html')


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
            user = authenticate(request, username=UN, password=PS)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'User credentials does not exist')
    return render(request, 'login.html')


def logoutpage(request):
    logout(request)
    return redirect('/')


@login_required(login_url='MovieApp:login')
def review_page(request, id):
    DE = Movie.objects.get(id=id)
    if request.method == "POST":
        U = request.user
        caption = request.POST.get('caption', )
        review = request.POST.get('review', )
        movie = DE.name
        RE = Review(user=U, caption=caption, review=review, movie=Movie.objects.get(name=movie))
        au = Review.objects.filter(movie=id).filter(user=U)
        if au.exists():
            messages.info(request, 'You have already submitted a Review')
        else:
            RE.save()
            return redirect('/')
    return render(request, 'reviewpage.html')


@login_required(login_url='MovieApp:login')
def re_delete(request, id):
    N = request.user
    if request.method == "POST":
        DE = Review.objects.get(id=id)
        print(DE.user, N)
        if DE.user == N:
            DE.delete()
            return redirect('/')
        else:
            messages.info(request, 'You are not authorized to delete this review')
    return render(request, 're_delete.html')


def search_result(request):
    query = request.GET.get('q', '').strip()
    M = []
    # The strip() method in Python is used to remove leading and trailing characters from a string. By default, it removes whitespace characters such as spaces, tabs, and newlines. However, it can also be used to remove other specified characters.
    if query:
        M = Movie.objects.filter(
            Q(user__username__icontains=query) |
            Q(name__icontains=query) |
            Q(desc__icontains=query) |
            Q(year__icontains=query) |
            Q(category__name__icontains=query) |
            Q(category__description__icontains=query) |
            # use small letter for category as it will raise error while running.
            Q(review__caption__icontains=query) |
            Q(review__review__icontains=query)
        ).distinct()
        print(M)
    #   The distinct() method removes duplicate rows from a DataFrame. It considers all columns in the DataFrame and returns only unique rows.
    return render(request, 'search.html', {'M': M, 'query': query})
