from rest_framework import viewsets, permissions
from .models import *
from .serializers import PropertySerializer, CollaborationSerializer, SlideSerializer, YourPerfectSerializer, SidebarCardSerializer, DamacSerializer, EmpoweringCommunitiesSerializer, UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdminOrReadOnly, IsAdminOrSelf, IsAdminUser


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(request, username=email, password=password)
            
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
    permission_classes = [AllowAny]  # Make public to avoid auth issues

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            user_data = {
                "id": user.id,
                "name": user.username,
                "email": user.email,
                "role": user.groups.first().name if user.groups.exists() else "user"
            }
            return Response({"user": user_data})
        else:
            return Response({"user": None}, status=401)
    


class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            user_data = {
                "id": user.id,
                "name": user.username,
                "email": user.email,
                "role": user.groups.first().name if user.groups.exists() else "user"
            }
            
            return Response({
                "user": user_data,
                "token": access_token
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]  # Public registration
        elif self.action == 'list':
            permission_classes = [AllowAny]  # Public user list (GET)
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrSelf]  # Admin or self
        else:  # retrieve
            permission_classes = [IsAdminOrSelf]  # Admin or self
        return [permission() for permission in permission_classes]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        print(f"Request data: {request.data}")
        print(f"Request files: {request.FILES}")
        print(f"Content type: {request.content_type}")
        
        if 'img' in request.FILES:
            print(f"Image file received: {request.FILES['img']}")
        else:
            print("No image file received")
        
        return super().create(request, *args, **kwargs)



class CollaborationViewSet(viewsets.ModelViewSet):
    queryset = Collaboration.objects.all()
    serializer_class = CollaborationSerializer
    permission_classes = [IsAdminOrReadOnly]



class SlideViewSet(viewsets.ModelViewSet):
    queryset = Slide.objects.all()
    serializer_class = SlideSerializer
    permission_classes = [IsAdminOrReadOnly]


class YourPerfectViewSet(viewsets.ModelViewSet):
    queryset = YourPerfect.objects.all()
    serializer_class = YourPerfectSerializer
    permission_classes = [IsAdminOrReadOnly]



class SidebarCardViewSet(viewsets.ModelViewSet):
    queryset = SidebarCard.objects.all()
    serializer_class = SidebarCardSerializer
    permission_classes = [IsAdminOrReadOnly]



class DamacViewSet(viewsets.ModelViewSet):
    queryset = Damac.objects.all()
    serializer_class = DamacSerializer
    permission_classes = [IsAdminOrReadOnly]



class EmpoweringCommunitiesViewSet(viewsets.ModelViewSet):
    queryset = EmpoweringCommunities.objects.all()
    serializer_class = EmpoweringCommunitiesSerializer
    permission_classes = [IsAdminOrReadOnly]
