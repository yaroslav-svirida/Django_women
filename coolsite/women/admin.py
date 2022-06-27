from django.contrib import admin

# Register your models here.
from .models import *

class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create')
    list_display_links = ( 'title', )
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ( 'name', )
    search_fields = ('name',)
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)
