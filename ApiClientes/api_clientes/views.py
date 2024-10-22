import timeit
from typing import Optional
from pydantic import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import api_clientes
from api_clientes.clients.client.models.queries import (
    QueryUserByTagModel,
    QueryUserModel,
)
from api_clientes.clients.client.models.usermodels import UserModel
from api_clientes.clients.datarepo import DataRepo
from api_clientes.pagination import CustomPagination
from api_clientes.serializers import ResponseSerializer
from api_clientes.utils.flatten_pydantic import flatten_pydantic


class Users(APIView):
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


class UsersByRegion(APIView):
    serializer_class = ResponseSerializer
    pagination_class = CustomPagination

    def get(self, request, region: str, tag: Optional[str] = None):
        timer = timeit.default_timer()
        DataRepo(api_clientes.redis_conn).get_data()
        try:
            (
                QueryUserModel(region=region)
                if tag is None
                else QueryUserByTagModel(region=region, tag=tag)
            )
        except ValidationError as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"errors": str(e)},
            )

        keys = api_clientes.redis_conn.smembers(f"{DataRepo.REDIS_REGION_KEY}:{region}")
        data = api_clientes.redis_conn.mget(keys)

        filtered_data = []
        for u in data:
            user = UserModel.model_validate_json(u)
            if user.location.region == region:
                if tag is not None:
                    if user.type == tag:
                        filtered_data.append(flatten_pydantic(user))
                        continue
                filtered_data.append(flatten_pydantic(user))

        pagination = self.pagination_class()
        paginated_users = pagination.paginate_queryset(filtered_data, request)

        print(f"{timeit.default_timer()-timer:.5f}")
        return pagination.get_paginated_response(
            data={"users": paginated_users},
        )
