from django.shortcuts import render, redirect
from .form import MovieForm
from . models import Movie

# Create your views here.
def index(request):
    movie=Movie.objects.all()
    return render(request,'index.html',{'M':movie})

def detail(request,movie_id):
    movie=Movie.objects.get(id=movie_id)
    return render(request,"detail.html",{'M':movie})

def add_movie(request):
    if request.method == "POST":
        name=request.POST.get('name',)
        desc = request.POST.get('desc', )
        year = request.POST.get('year', )
        img = request.FILES['img']
        movie=Movie(name=name,desc=desc,year=year,img=img)
        movie.save()
    return render(request,'add.html')

def Update(request,id):
    movie=Movie.objects.get(id=id)
    FM2=MovieForm(request.POST or None, request.FILES, instance=movie)
    if FM2.is_valid():
        FM2.save()
        return redirect('/')
    return render(request,'edit.html',{'FM2':FM2,'movie':movie})

def Delete(request,id):
    if request.method == "POST":
        DE=Movie.objects.get(id=id)
        DE.delete()
        return redirect('/')
    return render(request,'delete.html')