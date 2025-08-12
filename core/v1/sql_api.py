from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .services import get_category
from rest_framework.response import Response
from methodism import custom_response


class CategorySQLView(APIView):
    permission_classes = AllowAny,

    def get(self, request, pk=None):
        natija = get_category(pk)
        return Response(custom_response(False, natija, "Categriya Topilmadi!"),
                        status=200)




