from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import *
from products.serializer import *
from django.contrib.auth import authenticate, login, logout
import stripe


stripe.api_key = "sk_test_51NptrYSDCWX9Q5liyQZxbcCaR3l0YkvOyBBfX7vCNaA6FKhGchPSvHqehaUlTxrd0Hja6BLZPAcd03CpcasGk4Jo006S1ESYUw"

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
        try:
            user = get_object_or_404(User, id=request.session["id"])
            user_srlz = UserSerializer(user)
            return Response(user_srlz.data, status=status.HTTP_200_OK)
        except:
            pass
        return Response({"msg":""}, status=status.HTTP_401_UNAUTHORIZED)
        
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
        user = get_object_or_404(User, id=request.session["id"])
        cart_data = ProductCart.objects.filter(user_id=user)
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
    
class CartMultiView(APIView):
    
    def post(self, request):
        user = get_object_or_404(User, id=request.session["id"])
        ProductCart.objects.filter(user_id = user).delete()
        srlz_data = CartSerializer(data = request.data,many = True)
        if srlz_data.is_valid():
            srlz_data.save(user_id = user)
            return Response({'msg':'Successfully added items in cart'}, status=status.HTTP_201_CREATED)
        else:
            return Response(srlz_data.errors, status=status.HTTP_400_BAD_REQUEST)


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
    

class SimpleCheckout(APIView):
    def post(self, request):
        response = request.data
        print(response)
        try:
            data = stripe.checkout.Session.create(
                line_items= response['items'],
                mode="payment",
                customer_email=response['email'],
                success_url="http://localhost:3000/success",
                cancel_url="http://localhost:3000/cancel",
            )
            print(data)
            return Response({"data": data}, status=status.HTTP_201_CREATED)
        except:
            return Response({'msg': "Can't create session ID"}, status=status.HTTP_400_BAD_REQUEST)
class SaveOrder(APIView):
    def post(self, request):
        response = request.data
        session = stripe.checkout.Session.retrieve(response['session'])
        print(session)
        return Response({"data": session}, status=status.HTTP_200_OK)
