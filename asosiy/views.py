from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializer import *
import requests

class LoginView(APIView):
    def get(self, request):
        login = Login.objects.all()
        serializer = LoginSerializer(login, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        received_kod = request.data.get('kod')
        phone_number = request.data.get('phone')

        try:
            phone_obj = Kod.objects.get(tel=phone_number)
            response_data = {"exists": "Royhattan otgan mijoz"}
            status_code = status.HTTP_200_OK
        except Kod.DoesNotExist:
            # Bazada raqam yo'q, uni saqlash
            phone_obj = Kod(tel=phone_number, kod=received_kod)
            phone_obj.save()
            response_data = {"exists": "Yangi mijoz", "message": "Phone number saved"}
            status_code = status.HTTP_201_CREATED
        except Exception as e:
            response_data = {"error": str(e)}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        # SMS jonatish
        if status_code == status.HTTP_201_CREATED:
            sms_url = "https://notify.eskiz.uz/api/message/sms/send"
            sms_payload = {
                'mobile_phone': phone_number,
                'message': received_kod,
                'from': '4546',
                'callback_url': 'http://0000.uz/test.php'
            }
            sms_headers = {
                'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjQ4NjIsInJvbGUiOm51bGwsImRhdGEiOnsiaWQiOjQ4NjIsIm5hbWUiOiJZdW51c292IFNoZXJ6b2QgQmF4b2RpcmpvbiBvJ2cnbGkiLCJlbWFpbCI6InNoZXJ6b2R5dW51c292ZGV2QGdtYWlsLmNvbSIsInJvbGUiOm51bGwsImFwaV90b2tlbiI6bnVsbCwic3RhdHVzIjoiYWN0aXZlIiwic21zX2FwaV9sb2dpbiI6ImVza2l6MiIsInNtc19hcGlfcGFzc3dvcmQiOiJlJCRrIXoiLCJ1el9wcmljZSI6NTAsInVjZWxsX3ByaWNlIjoxMTUsInRlc3RfdWNlbGxfcHJpY2UiOm51bGwsImJhbGFuY2UiOjQ4ODUsImlzX3ZpcCI6MCwiaG9zdCI6InNlcnZlcjEiLCJjcmVhdGVkX2F0IjoiMjAyMy0wOC0yOFQwODozMTozMy4wMDAwMDBaIiwidXBkYXRlZF9hdCI6IjIwMjMtMDgtMjhUMDg6NDU6MDQuMDAwMDAwWiIsIndoaXRlbGlzdCI6bnVsbCwiaGFzX3BlcmZlY3R1bSI6MCwiYmVlbGluZV9wcmljZSI6bnVsbH0sImlhdCI6MTY5MzIyODExOCwiZXhwIjoxNjk1ODIwMTE4fQ.K9TqdXKs7yEV66-XSn28gwWJoEUx-vj6yZwFPUJPQUY"
            }

            # SMS jonatish so'rovi
            sms_response = requests.post(sms_url, headers=sms_headers, data=sms_payload)

            # SMS jonatish natijasini tekshirish
            if sms_response.status_code == 200:
                response_data["sms_status"] = "SMS jonatildi"
            else:
                response_data["sms_status"] = "SMS jonatishda xatolik yuzaga keldi"

        return Response(response_data, status=status_code)



class SMSApiView(APIView):
    def get(self, request):
        kod = Kod.objects.all()
        serializer = KodSerializer(kod, many=True)
        return Response(serializer.data)
    def post(self, request):
        received_kod = request.data.get('kod')
        phone = request.data.get('phone')

        # SMS jonatish
        url = "https://notify.eskiz.uz/api/message/sms/send"
        payload = {
            'mobile_phone': phone,
            'message': received_kod,
            'from': '4546',
            'callback_url': 'http://0000.uz/test.php'
        }
        headers = {
            'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjQ4NjIsInJvbGUiOm51bGwsImRhdGEiOnsiaWQiOjQ4NjIsIm5hbWUiOiJZdW51c292IFNoZXJ6b2QgQmF4b2RpcmpvbiBvJ2cnbGkiLCJlbWFpbCI6InNoZXJ6b2R5dW51c292ZGV2QGdtYWlsLmNvbSIsInJvbGUiOm51bGwsImFwaV90b2tlbiI6bnVsbCwic3RhdHVzIjoiYAWNlcnZlcjEiLCJjcmVhdGVkX2F0IjoiMjAyMy0wOC0yOFQwODozMTozMy4wMDAwMDBaIiwidXBkYXRlZF9hdCI6IjIwMjMtMDgtMjhUMDg6NDU6MDQuMDAwMDAwWiIsIndoaXRlbGlzdCI6bnVsbCwiaGFzX3BlcmZlY3R1bSI6MCwiYmVlbGluZV9wcmljZSI6bnVsbH0sImlhdCI6MTY5MzIyODExOCwiZXhwIjoxNjk1ODIwMTE4fQ.K9TqdXKs7yEV66-XSn28gwWJoEUx-vj6yZwFPUJPQUY"
        }
        response_sms = requests.post(url, headers=headers, data=payload)

        if response_sms.status_code == 200:
            # SMS muvaffaqiyatli yuborildi
            # Kodni saqlash
            serializer_data = {'kod': received_kod, 'tel': phone}
            serializer = KodSerializer(data=serializer_data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'SMS yuborildi va kod saqlandi.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Kodni saqlashda xatolik yuz berdi.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # SMS yuborilmadi yoki xatolik sodir bo'ldi
            return Response({'error': 'SMS yuborishda xatolik yuz berdi.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Kod_tekshirish(APIView):
    def get(self,request):
        kod = Kod.objects.all()
        serializer = KodSerializer(kod, many=True)
        return Response(serializer.data)
    def post(self, request):
        kod = request.data.get('code')

        # Barcha Kod obyektlarini olib olish
        kodlar = Kod.objects.all().values('kod')

        if any(kod == i['kod'] for i in kodlar):
            return Response({'message': 'Kod togri'}, status=status.HTTP_200_OK)

        return Response({'message': 'Kod noto\'g\'ri'}, status=status.HTTP_400_BAD_REQUEST)

class RegisterApiView(APIView):
    def get(self, reuqest):
        register = Register.objects.all()
        serializer = RegisterSerializer(register, many=True)
        return Response(serializer.data)
    def post(self, request):
        # POST so'rovi orqali malumotlarni olish
        username = request.data.get('username')
        phone_number = request.data.get('phone_number')
        category = request.data.get('tanlov')

        try:
            # Register jadvalida yangi obyektni yaratish va saqlash
            register_obj = Register(username=username, phone_number=phone_number, category=category)
            register_obj.save()

            # Muvaffaqiyatli saqlangan malumotni javob qilish
            return Response({'message': 'Malumot saqlandi.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Xatolik yuz berib, xatolik haqida xabar berish
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LocationList(APIView):
    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordAndProgramsView(APIView):
    def get(self, request):
        passwords = Password.objects.all()
        serializer = PasswordSerializer(passwords, many=True)
        return Response(serializer.data)

    def post(self, request):
        password_serializer = PasswordSerializer(data=request.data)
        if password_serializer.is_valid():
            password = password_serializer.save()

            apps_data = request.data.get('apps', [])
            for app_data in apps_data:
                Programs.objects.create(programs_id=password, **app_data)

            return Response(password_serializer.data, status=status.HTTP_201_CREATED)
        return Response(password_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# url = " https://notify.eskiz.uz/api/auth/login"
#
# payload={'email': 'sherzodyunusovdev@gmail.com',
# 'password': 'HlQXys4BvySyp3MhthHPq2Gie8l7G4M3ykpLZV2o'}
# files=[
#
# ]
# headers = {}
#
# response = requests.request("POST", url, headers=headers, data=payload, files=files)
#
# print(response.text)


# Create your views here.
