from django.shortcuts import render
from .models import CustomUser, Address
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import permissions
# Create your views here.

class RegisterApi(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'data':serializer.data,
                'token':token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoginApi(APIView):
    permission_classes = [permissions.AllowAny, ]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            return Response({
                'user':data['user'].username,
                'token':data['token'],
                'status':status.HTTP_200_OK

            })
        return Response({
            'errors': serializer.errors,
            'status':status.HTTP_400_BAD_REQUEST
        })

class LogautApi(APIView):
    permission_classes = [permissions.AllowAny, ]
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(
                {'msg':"siz dasturdan chiqdingiz", 'status':status.HTTP_200_OK}
            )
        except Exception as e:
            return Response(
                {'error': str(e),'status':status.HTTP_400_BAD_REQUEST}
            )
        


class ProfileApi(APIView):
    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(
            {
                'data':serializer.data,
                'status': status.HTTP_200_OK
            }
        )
    
    def patch(self, request):
        permission_classes = [permissions.AllowAny, ]
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'data':serializer.data,
                    'status':status.HTTP_200_OK
                }
        )
        return Response({'error':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})



