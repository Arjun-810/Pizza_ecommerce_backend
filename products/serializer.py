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
            "is_active"
        )

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
    

class CartSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(read_only = True, source='item_id.item_name')
    item_image = serializers.URLField(read_only = True, source= 'item_id.imageUrl')
    user_name = serializers.CharField(read_only = True, source='user_id.name')

    class Meta:
        model = ProductCart
        fields = '__all__'
