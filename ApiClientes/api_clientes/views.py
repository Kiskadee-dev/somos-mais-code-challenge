from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_clientes.serializers import UserModelSerializer
from api_clientes.clients.client.models.usermodels import UserModel


class Clientes(APIView):
    serializer_class = UserModelSerializer

    def get(self, request) -> Response:
        print(UserModel.model_json_schema())
        return Response(status=status.HTTP_200_OK)
