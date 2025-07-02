from django.urls import path
from . import views

app_name = 'MovieApp'

urlpatterns = [
    path('register/', views.register_page, name="register"),
    path('login/', views.loginpage, name="login"),
    path('logout/', views.logoutpage, name="logout"),
    path('add/', views.add_movie, name="add_movie"),
    path('search_result/', views.search_result, name="search_result"),
    # make sure you place the add url and search url before the allProdCat url or you will face the error because of search of category on running function.
    path('<slug:c_slug>/', views.allProdCat, name="product_by_category"),

    path('movie/<int:id>/', views.detail, name="detail"),
    path('Update/<int:id>/', views.Update, name='Update'),
    path('Delete/<int:id>/', views.Delete, name="Delete"),
    path('review/<int:id>/', views.review_page, name="review"),
    path('re_delete/<int:id>/', views.re_delete, name="re_delete"),
    path('', views.index, name="index")
]
