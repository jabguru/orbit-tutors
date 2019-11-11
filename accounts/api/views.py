from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from accounts.models import UserProfile

from accounts.api.serializers import RegistrationSerializer, AccountPropertiesSerializer, UserProfileSerializer
from rest_framework.authtoken.models import Token

from rest_framework.authentication import TokenAuthentication


@api_view(['POST', ])
def registration_view(request):
    if request.POST:
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'Successfully registered new user'
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token

        else:
            data = serializer.errors

        return Response(data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def account_properties_view(request):
    try:
        account = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountPropertiesSerializer(account)
        return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def update_account_view(request):
    try:
        account = request.user
        profile = UserProfile.objects.get(user=account)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = AccountPropertiesSerializer(account, data=request.data)
        profile_serializer = UserProfileSerializer(profile, data=request.data)
        data = {}

        if serializer.is_valid() and profile_serializer.is_valid():
            serializer.save()
            profile_serializer.save()
            data['response'] = 'Account Update Successful'
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
