from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.
class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title ', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create',
              'time_update')  # we choose the fields which we can edit
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')  # this fields we can't edit, just for reading

    # we doing a photo display
    def get_html_photo(self, object):  # object refers to an object of the women class
        if object.photo:
            return mark_safe(f'<img src="{object.photo.url}" width=50 height = 50>')

    get_html_photo.short_description = 'Image'  # we rename this field on "Image"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(AboutModel)
admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Admin panel'
admin.site.site_header = 'Admin panel'
