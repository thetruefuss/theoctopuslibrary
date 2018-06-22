from django.contrib import admin

from .models import Book, Photo


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'submitter', 'created', 'is_active')
    date_hierarchy = 'created'
admin.site.register(Book, BookAdmin)  # noqa: E305


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('book', 'photo', 'created')
    date_hierarchy = 'created'
admin.site.register(Photo, PhotoAdmin)  # noqa: E305
