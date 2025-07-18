import random
import uuid

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from base.helper import validate_phone
from core.models import User, OTP
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from base.costum import BearerAuth
import bcrypt


class StepOne(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data

        if "phone" not in data:
            return Response({"error": "phone required"}, status=400)

        # agar email bo'lsa email validation, phone phonevalidation
        if not validate_phone(data['phone']):
            return Response({"Error": "Raqamni tog'ri kiriting!"}, status=400)

        code = random.randint(100_000, 999_999)
        # shu yerda sms yoki emailga yuboriladi
        print(code)
        secure_password = str(code).encode("utf-8")
        salt = bcrypt.gensalt()  # Generate a random salt
        hashed_password = bcrypt.hashpw(secure_password, salt)  # Hash the password with the salt

        otp = OTP.objects.create(key=hashed_password, mobile=data['phone'])

        return Response({
            "otp_token": otp.key
        })


class StepTwo(APIView):
    permission_classes = AllowAny,

    def get(self, request):
        return Response({"javob": "Endi Getni ushlaydi"})

    def post(self, request):
        data = request.data

        if "otp" not in data.keys() or "otp_token" not in data.keys():
            return Response({"error": "otp and otp_token required"}, status=400)
        token = data['otp_token'].encode("utf-8")
        otp = data['otp']

        otp = OTP.objects.filter(key=token).first()
        if not otp:
            return Response({"error": "otp_token not found"}, status=404)

        if otp.is_expired or otp.is_verified:
            return Response({"error": "Token Allaqachon Eskirgan yoki Foydalanib bo'lingan!"}, status=403)

        if not otp.check_expire_date():
            return Response({"error": "Tokenga ajratilgan vaqt tugadi!"}, status=403)

        decrypt = bcrypt.checkpw(str(data['otp']).encode('utf-8'), token)
        if not decrypt:
            otp.tries += 1
            otp.save()
            return Response({"error": "Xato Kod"}, status=401)

        otp.is_verified = True
        otp.is_expired = True
        otp.save()

        user = User.objects.filter(phone=otp.mobile).first()

        return Response({
            "is_registered": bool(user)
        })


class RegisterView(GenericAPIView):
    permission_classes = AllowAny,

    def post(self, request) -> Response:
        """
            request -> API dan zsdkflasn
            asdfasdf
            asdfasdf


        """

        data = request.data
        fio = data.get('fio', None)
        password = data.get('password', None)
        phone = data.get('phone', None)
        otp_token = data.get("otp_token")

        if None in [fio, password, phone, otp_token]:
            return Response({"Error": 'Malumotlarni toliq kiriting'}, status=HTTP_400_BAD_REQUEST)

        otp = OTP.objects.filter(key=otp_token).first()
        if not otp.is_verified or str(otp.mobile) != str(phone):
            return Response({"Error": "Ma`lumotlar tog'ri kiritilmagan!"}, status=HTTP_400_BAD_REQUEST)

        user = User.objects.filter(phone=phone).first()
        if user:
            return Response({"Error": "Bu raqam allaqachon Ro'yxatdan o'tgan"}, status=400)

        # create user
        # version 1
        # data.pop("fio")
        # data.pop("password")
        # data.pop("phone")
        # user = User.objects.create_user(phone=phone,
        #                                 password=password,
        #                                 fio=fio,
        #                                 **data)

        # version 2
        user = User.objects.create_user(**data)

        token = Token.objects.get_or_create(user=user,
                                            key=uuid.uuid4())[0]  # natija-> tuple (token, True)
        return Response({
            "Succes": "User Registered",
            "user": user.get_response(token.key),
        }, status=HTTP_201_CREATED)


class LogoutView(GenericAPIView):
    authentication_classes = BearerAuth,
    permission_classes = IsAuthenticated,

    def post(self, request):
        user = request.user
        token = Token.objects.filter(user=user).first()

        if token:
            token.delete()

        return Response({"Success": "User Logged Out"})


class LoginView(GenericAPIView):
    permission_classes = AllowAny,



    def post(self, request):
        data = request.data

        phone = data.get("phone", None)
        pasword = data.get("password", None)
        otp_token = data.get("otp_token")

        if None in [pasword, phone]:
            return Response({"error": "phone and password required"}, status=400)

        otp = OTP.objects.filter(key=otp_token).first()
        if not otp.is_verified or str(otp.mobile) != str(phone):
            return Response({"Error": "Ma`lumotlar tog'ri kiritilmagan!"}, status=HTTP_400_BAD_REQUEST)

        user = User.objects.filter(phone=phone).first()
        if not user:
            return Response({"error": "Phone or password error"}, status=404)

        if not user.check_password(str(pasword)):
            return Response({"error": "Phone or password error"}, status=404)

        token = Token.objects.get_or_create(user=user)[0]  # 2ta narsa qaytaradi (token.obj, False)

        return Response({
            "succes": "User Logged",
            "access_token": token.key,
            "user": user.get_response()
        })
