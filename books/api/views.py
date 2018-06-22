from books.models import Book
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     RetrieveUpdateAPIView, UpdateAPIView)
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .pagination import BookLimitOffsetPagination, BookPageNumberPagination
from .permissions import IsSubmitterOrReadOnly
from .serializers import (BookCreateUpdateSerializer, BookListSerializer,
                          BookRetrieveSerializer)


# untested view
class BookCreateAPIView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(submitter=self.request.user)


class BookListAPIView(ListAPIView):
    serializer_class = BookListSerializer
    pagination_class = BookPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']

    def get_queryset(self, *args, **kwargs):
        queryset_list = Book.objects.all()
        location_query = self.request.GET.get('location', '')
        category_query = self.request.GET.get('category', '')
        if location_query or category_query:
            queryset_list = queryset_list.filter(
                location__icontains=location_query,
                category__icontains=category_query
            )
        return queryset_list


class BookRetrieveAPIView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookRetrieveSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


# untested view
class BookUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsSubmitterOrReadOnly]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def perform_update(self, serializer):
        serializer.save(submitter=self.request.user)


class BookDestroyAPIView(DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookRetrieveSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsSubmitterOrReadOnly]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
