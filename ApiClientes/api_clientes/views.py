from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_clientes.clients.datarepo import DataRepo
from api_clientes.pagination import CustomPagination
from api_clientes.serializers import ResponseSerializer
import timeit

from api_clientes.utils.flatten_pydantic import flatten_pydantic


class Clientes(APIView):
    serializer_class = ResponseSerializer
    pagination_class = CustomPagination

    def get(self, request):
        start = timeit.default_timer()
        users = DataRepo().get_data()
        print("The difference of time is :", timeit.default_timer() - start)
        pagination = self.pagination_class()
        paginated_users = pagination.paginate_queryset(users, request)

        if paginated_users is not None:
            print(len(paginated_users))
            return pagination.get_paginated_response(
                {"users": [flatten_pydantic(u) for u in paginated_users]}
            )

        return Response(
            status=status.HTTP_200_OK,
            data={"users": [u.model_dump_json() for u in users]},
        )
