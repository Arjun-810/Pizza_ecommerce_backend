from rest_framework import serializers
from .models import *

class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('ingredient_id', 'ingedrient_name', 'status')

class MenuItemSerializer(serializers.ModelSerializer):
    ingredients = IngredientsSerializer(many=True)

    class Meta:
        model = MenuItem
        fields = ('id', 'imageUrl', 'ingredients', 'item_name', 'soldOut', 'unitPrice', 'status')


    def to_representation(self, instance):
        data = super(MenuItemSerializer, self).to_representation(instance)
        data['ingredients'] = [ingredient['ingedrient_name'] for ingredient in data['ingredients']]
        return data
    

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        exclude = (
            "last_login",
            "is_superuser",
            "is_staff",
            "date_joined",
            "groups",
            "user_permissions",
            "last_name",
            "first_name",
        )

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        # Remove the 'password' field from validated_data if it's not provided in the request
        password = validated_data.pop('password', None)

        # Update the instance with the remaining validated_data
        instance = super(UserSerializer, self).update(instance, validated_data)

        # Set the password if it's provided
        if password is not None:
            instance.set_password(password)
            instance.save()

        return instance
    

class CartSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(read_only = True, source='item_id.item_name')
    unit_price = serializers.CharField(read_only = True, source='item_id.unitPrice')
    item_image = serializers.URLField(read_only = True, source= 'item_id.imageUrl')
    user_name = serializers.CharField(read_only = True, source='user_id.name')

    class Meta:
        model = ProductCart
        fields = '__all__'


class OrderItemsSerializer(serializers.ModelSerializer):
    unit_price = serializers.CharField(read_only = True, source='item_id.unitPrice')
    item_image = serializers.URLField(read_only = True, source= 'item_id.imageUrl')
    item_name = serializers.CharField(read_only = True, source='item_id.item_name')
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemsSerializer(many=True, source='order_map')
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_map')
        order = Order.objects.create(**validated_data)

        for item_data in order_items_data:
            OrderItem.objects.create(order_id=order, **item_data)

        return order
    
class OrderPutSerialier(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    