from django.shortcuts import get_object_or_404
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
        print("data222 = ",request.data)
        user_exist = User.objects.filter(username = request.data['username']).exists()
        if user_exist:
            return Response({'msg': 'User already exist'}, status=status.HTTP_400_BAD_REQUEST)
        print("data = ",request.data)
        user_srlz = UserSerializer(data=request.data)
        if user_srlz.is_valid():
            user_srlz.save()
        else:
            return Response(user_srlz.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'User Successfully Creadted'})


class Login(APIView):
    def get(self, request):
        user = get_object_or_404(User, id=request.session["id"])
        user_srlz = UserSerializer(user)
        return Response(user_srlz.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session["id"] = request.user.id
            user = User.objects.get(id = request.user.id)
            srlz = UserSerializer(user)
            return Response(srlz.data, status=status.HTTP_200_OK)
        else:
            return Response({'msg':'User Not found with this credentials'}, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):

    def get(self, request):
        logout(request)
        return Response()


class CartView(APIView):

    def get(self,request):
        cart_data = ProductCart.objects.all()
        srlz_data = CartSerializer(cart_data, many=True)
        return Response(srlz_data.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = get_object_or_404(User, id=request.session["id"])
        srlz_data = CartSerializer(data = request.data)
        if srlz_data.is_valid():
            srlz_data.save(user_id = user)
            return Response({'msg':'Successfully added items in cart'}, status=status.HTTP_201_CREATED)
        else:
            return Response(srlz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = get_object_or_404(User, id=request.session["id"])
        try:
            ProductCart.objects.filter(user_id = user).delete()
            return Response({'msg': 'Cart deleted successfully'}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
class CartOperation(APIView):
    def put(self,request, pk):
        try:
            cart = ProductCart.objects.get(cart_id=pk)
        except:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        srlz_data = CartSerializer(cart, data=request.data,partial = True)
        if srlz_data.is_valid():
            srlz_data.save()
            return Response({'msg': 'Cart updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(srlz_data.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        try:
            cart = ProductCart.objects.get(cart_id=pk)
        except:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        cart.delete()
        return Response({'msg': 'Cart deleted successfully'}, status=status.HTTP_200_OK)