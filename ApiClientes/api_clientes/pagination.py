from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "pageNumber"
    page_size_query_param = "pageSize"
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response(
            {
                "totalCount": self.page.paginator.count,
                "pageNumber": self.page.number,
                "totalPages": self.page.paginator.num_pages,
                "pageSize": self.get_page_size(self.request),
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )

    def get_page_size(self, request):
        page_size = super().get_page_size(request)
        print(f"Page size used: {page_size}")  # Debugging
        return page_size
