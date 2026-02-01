from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'properties', PropertyViewSet)
router.register(r'collaborations', CollaborationViewSet)
router.register(r'slides', SlideViewSet)
router.register(r'yourperfect', YourPerfectViewSet)
router.register(r'sidebarcards', SidebarCardViewSet)
router.register(r'damac', DamacViewSet)
router.register(r'empoweringcommunities', EmpoweringCommunitiesViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),

]
