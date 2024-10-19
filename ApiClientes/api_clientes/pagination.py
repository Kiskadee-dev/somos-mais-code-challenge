from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    query_param = "pageNumber"
    size_param = "pageSize"
    page_size = 10
    max_page_size = 100
