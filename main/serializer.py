from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
import re

User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'phone_number', 'email', 'password')

    def validate(self, data):
        phone = data.get('phone_number')
        try:
            phone_number = User.object.filter(phone_number=phone)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            phone_number = None
        if phone_number:
            raise ValidationError({"error": "phone number already exists"})
        if phone:
            phone_regex = "^[6789]\d{9}$"
            phone_valid = re.compile(phone_regex)
            if not phone_valid.match(phone):
                raise ValidationError({"error": "Invalid Phone number"})
            else:
                return data
        raise ValidationError({"error": "Invalid Phone number"})


class LoginSerializer(serializers.ModelSerializer):
    """serializer for Login using otp"""
    phone_number = serializers.CharField(validators=None)
    password = serializers.CharField(allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ['phone_number', 'password']

    def validate(self, data):
        phone_number = data.get('phone_number')
        entered_password = data.get('password')  # jsh
        if phone_number:
            phone_regex = "^[6789]\d{9}$"
            phone_valid = re.compile(phone_regex)
            if not phone_valid.match(phone_number):
                raise ValidationError({"error": "Invalid Phone number"})
        try:
            user = User.object.get(phone_number=phone_number)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if not user or user is None:
            raise ValidationError({'error': "Phone number doesn't exist"})

        if entered_password == user.password:
            return data
        else:
            raise ValidationError({'error': "password not matched"})


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'phone_number', 'email', 'date_joined')


class AddItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddItem
        fields = ('id', 'user', 'item_name', 'item_quantity', 'item_status', 'date', 'date_str')
        read_only_fields = ('user',)


class SavedItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Savedlist
        fields = '__all__'
        read_only_fields = ('user',)

class ListSavedItemSerializer(serializers.ModelSerializer):
    item = AddItemSerializer()

    class Meta:
        model = Savedlist
        fields = '__all__'