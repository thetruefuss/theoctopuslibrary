from books.models import Book, Photo
from rest_framework import serializers


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('photo',)


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    book_photos = PhotoSerializer(required=False, many=True)

    class Meta:
        model = Book
        fields = (
            'title', 'description', 'category',
            'is_free', 'price', 'book_photos',
        )

    def create(self, validated_data):
        print(validated_data)
        book_photos_data = validated_data.pop('book_photos')
        book = Book.objects.create(**validated_data)
        for book_photo_data in book_photos_data:
            Photo.objects.create(book=book, **book_photo_data)
        return book

    def update(self, validated_data):
        return validated_data


class BookListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='books-api:books_retrieve',
        lookup_field='slug'
    )
    book_photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = (
            'url', 'title', 'slug', 'category', 'is_free',
            'price', 'location', 'book_photos',
        )


class BookRetrieveSerializer(serializers.ModelSerializer):
    book_photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = (
            'title', 'slug', 'category', 'is_free',
            'price', 'submitter', 'location', 'book_photos',
        )
