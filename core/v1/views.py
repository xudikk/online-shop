from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED
from rest_framework.generics import GenericAPIView, ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from .serializer import CategorySerializer, Category, ProductSerializer
from ..models import Product
from base.costum import BearerAuth


class CategoryViews(GenericAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = CategorySerializer
    queryset = Category.objects.all
    authentication_classes = BearerAuth,

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={201: CategorySerializer, 400: 'Bad Request'},
    )
    def get_object(self, id):
        return Category.objects.get(id=id)

    def get(self, request, id=None):
        print("\n\n", request.user, "\n\n")

        status = HTTP_200_OK
        if id:
            bitta_element = self.get_object(id)
            if not bitta_element:
                status = HTTP_404_NOT_FOUND
                data = {"error": "Bundan Kategoriya Topilmadi!"}
            else:
                data = bitta_element.get_response()
            return Response(data, status=status)
        else:
            data = [x.get_response() for x in self.queryset()]

        return Response({
            "natija": data
        }, status=status)

    def post(self, request):
        "asosan yangi narsa qo'shish uchun ishlatiladi!"
        data = request.data
        print(data)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "result": "Success",
            "ctg": serializer.data
        }, status=HTTP_201_CREATED)

    def put(self, request, id):
        ctg = self.get_object(id)
        if not ctg:
            return Response({
                "Error": "Categoriya Topilmadi"
            }, status=404)
        data = request.data
        serializer = self.serializer_class(data=data, instance=ctg)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "result": "Success",
            "ctg": serializer.data
        }, status=200)

    def patch(self, request, id):
        ctg = self.get_object(id)
        if not ctg:
            return Response({
                "Error": "Categoriya Topilmadi"
            }, status=404)
        data = request.data
        serializer = self.serializer_class(data=data, instance=ctg, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "result": "Success",
            "ctg": serializer.data
        }, status=200)

    def delete(self, request, id):
        ctg = self.get_object(id)
        try:
            ctg.delete()
        except:
            pass

        return Response({
            "result": "Deleted Successfully"
        }, status=200)


class ProductView(ListCreateAPIView,
                  UpdateAPIView, DestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = AllowAny,
    queryset = Product.objects.all()

    # def get_object(self, ):


class NewApi(APIView):
    permission_classes = AllowAny,

    def get(self, request):
        return Response({"javob": "Bu get zaprosi"})
