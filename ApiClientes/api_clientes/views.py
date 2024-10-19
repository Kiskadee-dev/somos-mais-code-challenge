from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_clientes.pagination import CustomPagination
from api_clientes.serializers import ListOfUsersSerializer
from api_clientes.clients.client.get_users import get_users


class Clientes(APIView):
    serializer_class = ListOfUsersSerializer
    pagination_class = CustomPagination

    def get(self, request):
        users = get_users()
        pagination = self.pagination_class()
        paginated_users = pagination.paginate_queryset(users, request)

        if paginated_users is not None:
            return pagination.get_paginated_response(
                [u.model_dump_json() for u in paginated_users]
            )

        return Response(
            status=status.HTTP_200_OK,
            data=[u.model_dump_json() for u in users],
        )
