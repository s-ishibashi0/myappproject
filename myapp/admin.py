from django.contrib import admin

# Register your models here.
from .models import Category, MyappPost


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


admin.site.register(Category, CategoryAdmin)


class MyappPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


admin.site.register(MyappPost, MyappPostAdmin)
