from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_clientes.serializers import ListOfUsersSerializer
from api_clientes.clients.client.get_users import get_users


class Clientes(APIView):
    serializer_class = ListOfUsersSerializer

    def get(self, request):
        users = get_users()
        return Response(
            status=status.HTTP_200_OK, data=[u.model_dump_json() for u in users]
        )
