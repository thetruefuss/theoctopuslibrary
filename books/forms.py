from django import forms

from .models import Book, Photo


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'category', 'description', 'is_free', 'price', )


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('photo', )
