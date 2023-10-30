from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .Serializers import *
from .models import *

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username, 'id': user.id})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):

    print("ij")
    return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

# endpoint qui récupére le nom et id d'utilisateur





class GetICImages(generics.ListAPIView):
    permission_classes = []
    queryset = Images.objects.filter(visible=True)
    serializer_class = ICSerializer




class AddClientView(generics.CreateAPIView):
    queryset = Clients.objects.all()
    serializer_class = AddClientsSerializer








