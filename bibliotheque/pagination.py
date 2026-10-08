from rest_framework.pagination import PageNumberPagination

class LivrePagination(PageNumberPagination):
    page_size = 5