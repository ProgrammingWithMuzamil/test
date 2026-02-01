from rest_framework import viewsets
from .models import *
from .serializers import PropertySerializer, CollaborationSerializer, SlideSerializer, YourPerfectSerializer, SidebarCardSerializer, DamacSerializer, EmpoweringCommunitiesSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(email=email, password=password)
            
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                user_data = {
                    "user": {
                        "id": user.id,
                        "name": user.username, 
                        "email": user.email,
                        "role": user.groups.first().name if user.groups.exists() else "user"  
                    },
                    "token": access_token
                }

                return Response(user_data, status=status.HTTP_200_OK)

            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_data = {
            "id": user.id,
            "name": user.username,
            "email": user.email,
            "role": user.groups.first().name if user.groups.exists() else "user"
        }
        return Response({"user": user_data})
    


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer



class CollaborationViewSet(viewsets.ModelViewSet):
    queryset = Collaboration.objects.all()
    serializer_class = CollaborationSerializer



class SlideViewSet(viewsets.ModelViewSet):
    queryset = Slide.objects.all()
    serializer_class = SlideSerializer


class YourPerfectViewSet(viewsets.ModelViewSet):
    queryset = YourPerfect.objects.all()
    serializer_class = YourPerfectSerializer



class SidebarCardViewSet(viewsets.ModelViewSet):
    queryset = SidebarCard.objects.all()
    serializer_class = SidebarCardSerializer



class DamacViewSet(viewsets.ModelViewSet):
    queryset = Damac.objects.all()
    serializer_class = DamacSerializer



class EmpoweringCommunitiesViewSet(viewsets.ModelViewSet):
    queryset = EmpoweringCommunities.objects.all()
    serializer_class = EmpoweringCommunitiesSerializer
