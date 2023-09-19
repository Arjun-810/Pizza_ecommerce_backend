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
        user_exist = User.objects.filter(username = request.data['username']).exists()
        if user_exist:
            user_inactive = User.objects.filter(username = request.data['username'],is_active = 0).exists()
            if user_inactive:
                data = User.objects.get(username = request.data['username'],is_active = 0)
                request.data["is_active"] = 1
                srlz_data = UserSerializer(instance=data, data=request.data, partial=True)
                if srlz_data.is_valid():
                    srlz_data.save()
                return Response({'msg': 'User Successfully Creadted'})
            return Response({'msg': 'User already exist'}, status=status.HTTP_400_BAD_REQUEST)
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
            data = user_srlz.data
            data["email"] = data['username']
            return Response(data, status=status.HTTP_200_OK)
        except:
            pass
        return Response({"msg":""}, status=status.HTTP_401_UNAUTHORIZED)
        
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password,is_active = 1)
        if user is not None:
            login(request, user)
            request.session["id"] = request.user.id
            user = User.objects.get(id = request.user.id)
            srlz = UserSerializer(user)
            data = srlz.data
            data["email"] = data['username']
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'msg':'User Not found with this credentials'}, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):

    def get(self, request):
        logout(request)
        return Response()


class CartView(APIView):

    def get(self,request):
        if "id" not in request.session:
            return Response({'error': 'User not Login'}, status=status.HTTP_401_UNAUTHORIZED)
        user = get_object_or_404(User, id=request.session["id"])
        cart_data = ProductCart.objects.filter(user_id=user)
        srlz_data = CartSerializer(cart_data, many=True)
        return Response(srlz_data.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if "id" not in request.session:
            return Response({'error': 'User not Login'}, status=status.HTTP_401_UNAUTHORIZED)
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

    def get(self, request):
        order_data = Order.objects.filter(user_id = request.session["id"])
        order_srlz = OrderSerializer(order_data, many = True)
        return Response(order_srlz.data , status=status.HTTP_200_OK)
    def post(self, request):
        response = request.data
        if "id" not in request.session:
            user_exist = User.objects.filter(username = request.data['email']).exists()
            if user_exist:
                pass
            else:
                print("test ")
                user_data = {}
                user_data['name'] = response['name']
                user_data['username'] = request.data['email']
                user_data['contact_number'] = request.data['phone']
                user_data['password'] = "123"
                user_data['is_active'] = 0
                user_srlz = UserSerializer(data=user_data)
                if user_srlz.is_valid():
                    user_srlz.save()
            user = get_object_or_404(User, username = request.data['email'])
        else:
            user = get_object_or_404(User, id=request.session["id"])
        # try:
        data = stripe.checkout.Session.create(
            line_items= response['items'],
            mode="payment",
            customer_email=response['email'],
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel",
        )
        order_data = {}
        order_data['total_amount'] = data['amount_total']
        order_data['contact_no'] = response['phone']
        order_data['client_name'] = response['name']
        order_data['delivery_address'] = response['address']
        order_data['order_items'] = response['products']
        order_data['stripe_session_id'] = data['id']
        order_data['is_priority'] = response['priority']
        srlz_data = OrderSerializer(data = order_data)
        if srlz_data.is_valid():
            srlz_data.save(user_id = user)
            return Response({"data": data}, status=status.HTTP_201_CREATED)
        return Response(srlz_data.errors, status=status.HTTP_400_BAD_REQUEST)
        # except:
        #     return Response({'msg': "Can't create session ID"}, status=status.HTTP_400_BAD_REQUEST)
        

class SaveOrder(APIView):
    def post(self, request):
        response = request.data
        session = stripe.checkout.Session.retrieve(response['session'])
        data = Order.objects.get(stripe_session_id = response['session'])
        srlz_data = OrderPutSerialier(instance=data, data={'order_status': session['payment_status']}, partial=True)
        if srlz_data.is_valid():
            srlz_data.save()
            if "id" in request.session:
                cart = ProductCart.objects.filter(user_id = request.session['id']).delete()
            return Response({"data": srlz_data.data}, status=status.HTTP_200_OK)
        return Response(srlz_data.errors, status=status.HTTP_400_BAD_REQUEST)

