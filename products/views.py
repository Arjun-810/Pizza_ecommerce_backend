from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import *
from products.serializer import *
from django.contrib.auth import authenticate, login, logout

class MenuItemList(APIView):
    def get(self, request):
        queryset = MenuItem.objects.all()
        srlz = MenuItemSerializer(queryset,many = True)
        return Response(srlz.data, status=status.HTTP_200_OK)


class Register(APIView):

    def get(self, request):
        user_data = User.objects.all()
        user_srlz = UserSerializer(user_data, many = True)
        return Response(user_srlz.data , status=status.HTTP_200_OK)
    
    def post(self, request):
        user_exist = User.objects.filter(email = request.data['email']).exists()
        if user_exist:
            return Response({'msg': 'User already exist'}, status=status.HTTP_400_BAD_REQUEST)
        user_srlz = UserSerializer(data=request.data)
        if user_srlz.is_valid():
            user_srlz.save()
        else:
            return Response(user_srlz.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'User Successfully Creadted'})


class Login(APIView):
    def post(self, request):
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'msg': "Successfully Loged in"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'msg':'User Not found with this credentials'}, status=status.HTTP_400_BAD_REQUEST)
