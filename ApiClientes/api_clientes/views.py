from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import api_clientes
from api_clientes.clients.datarepo import DataRepo
from api_clientes.pagination import CustomPagination
from api_clientes.serializers import ResponseSerializer

from api_clientes.utils.flatten_pydantic import flatten_pydantic


class Clientes(APIView):
    serializer_class = ResponseSerializer
    pagination_class = CustomPagination

    def get(self, request):
        users = DataRepo(api_clientes.redis_conn).get_data()
        pagination = self.pagination_class()
        paginated_users = pagination.paginate_queryset(users, request)

        if paginated_users is not None:
            return pagination.get_paginated_response(
                {"users": [flatten_pydantic(u) for u in paginated_users]}
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data={"users": []},
        )
