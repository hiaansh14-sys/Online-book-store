from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author','cover_image', 'price', 'category']
    list_filter = ['category', 'price']
    search_fields = ['title', 'author']

admin.site.register(Category)