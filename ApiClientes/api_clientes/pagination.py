from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):
    default_limit = 10

    def get_paginated_response(self, data):
        return Response(
            {
                "totalCount": self.count,
                "pageNumber": (self.offset // self.limit) + 1,
                "pageSize": self.limit,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
