from django.shortcuts import render
from .models import User
from .serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions, status
from .token import get_tokens_for_user
from .permission import *
from threading import Thread
from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
import re
from django.contrib.auth import login, logout


# Create your views here.
class UserAPIVIEW(APIView):
    permission_classes = [ReadOnly,]

    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            user_data = User.object.get(id=id)
            serialized_user_data = UserDetailSerializer(user_data)
            return Response(serialized_user_data.data)
        user_data = User.object.all()
        serialized_user_data = UserDetailSerializer(user_data, many=True)
        return Response(serialized_user_data.data)


class UserSignupAPIVIEW(APIView):
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serialized_data = UserSignupSerializer(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response({'msg': 'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        user = User.object.get(phone_number=phone_number)
        user_id = user.id

        try:
            receiver = User.object.get(id=user_id)
        except(TypeError, OverflowError, ValueError):
            receiver = None

        refresh, access = get_tokens_for_user(receiver)
        return Response({'info': 'successful!', 'user_id': user.id, 'phone': user.phone_number, 'email': user.email,
                        'refresh': refresh, 'access': access},
                        status=status.HTTP_201_CREATED)

class ItemView(APIView):
    permission_classes = [ReadOnly, ]

    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            item_data = AddItem.object.get(id=id)
            serialized_item_data = AddItemSerializer(item_data)
            return Response(serialized_item_data.data)
        item_data = AddItem.object.all()
        serialized_item_data = AddItemSerializer(item_data, many=True)
        return Response(serialized_item_data.data)


class ItemReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = AddItem.objects.all()
  serializer_class = AddItemSerializer




class AddItemView(viewsets.ModelViewSet):
    serializer_class = AddItemSerializer
    permission_classes = (permissions.IsAuthenticated, IsUser)
    queryset = AddItem.objects.all()

    def list(self, request):
        queryset = AddItem.objects.filter(user=request.user.id)
        serializer = AddItemSerializer(queryset, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def perform_create(self, serializer):

        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)




class SavedItemView(viewsets.ModelViewSet):
    serializer_class = SavedItemSerializer
    permission_classes = (permissions.IsAuthenticated, IsUser)
    queryset = Savedlist.objects.all()

    def list(self, request):
        queryset = Savedlist.objects.filter(user=request.user.id)
        serializer = ListSavedItemSerializer(queryset, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def perform_create(self, serializer):

        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)



def Home(request):
    return render(request, 'index.html')

def AddItem(request):
    return render(request, 'add.html')

def SavedItem(request):
    pass

def Loginhtml(request):
    return render(request, 'login.html')

def Signuphtml(request):
    return render(request, 'signup.html')


class LogoutView(APIView):
    """
    logout view.Only authenticated user can access this url(by default)
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({'message':'successfully logged out'},
                        status=status.HTTP_200_OK)


