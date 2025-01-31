from django.urls import path
from . import views

app_name = 'MovieApp'

urlpatterns = [
    path('',views.index,name="index"),
    path('movie/<int:movie_id>/',views.detail,name="detail"),
    path("add/",views.add_movie,name="add_movie"),
    path('Update/<int:id>/',views.Update,name='Update'),
    path('Delete/<int:id>/',views.Delete,name="Delete")
]