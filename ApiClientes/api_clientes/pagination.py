from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    default_limit = 10
    page_query_param = "pageNumber"
    page_size_query_param = "pageSize"

    def get_paginated_response(self, data):
        return Response(
            {
                "totalCount": self.page.paginator.count,
                "pageNumber": self.page.number,
                "totalPages": self.page.paginator.num_pages,
                "pageSize": self.page_size,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
