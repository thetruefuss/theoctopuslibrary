from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)


class BookLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 20


class BookPageNumberPagination(PageNumberPagination):
    page_size = 20
