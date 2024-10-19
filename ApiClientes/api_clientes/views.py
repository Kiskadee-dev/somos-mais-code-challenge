from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_clientes.serializers import ClientSerializer


class Clientes(APIView):
    serializer_class = ClientSerializer

    def get(self, request) -> Response:
        return Response(status=status.HTTP_200_OK)
