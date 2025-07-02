from django.contrib import admin
from .models import Category, Movie, Review


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    # PREPOPULATED FILED IS USED TO SET SLUG FILED IN ADMIN AND TO LIST CATEGORY URL
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)

admin.site.register(Movie)
admin.site.register(Review)
