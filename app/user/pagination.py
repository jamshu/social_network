from rest_framework.pagination import PageNumberPagination


class UserSearchPagination(PageNumberPagination):
    page_size = 10

