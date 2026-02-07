from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PropertyViewSet, CollaborationViewSet, SlideViewSet, 
    YourPerfectViewSet, SidebarCardViewSet, DamacViewSet, 
    EmpoweringCommunitiesViewSet, UserViewSet, AgentViewSet, 
    CMSSettingsViewSet, PublicAgentViewSet, LoginView, 
    RegisterView, UserProfileView, LeadViewSet, 
    AgentLeadViewSet, PublicLeadViewSet, AdminAnalyticsViewSet,
    AgentAnalyticsViewSet, HeroViewSet, PublicHeroViewSet,
    DealViewSet, AgentRevenueView
)

router = DefaultRouter()
router.register(r'properties', PropertyViewSet)
router.register(r'collaborations', CollaborationViewSet)
router.register(r'slides', SlideViewSet)
router.register(r'yourperfect', YourPerfectViewSet)
router.register(r'sidebarcard', SidebarCardViewSet)
router.register(r'damac', DamacViewSet)
router.register(r'empoweringcommunities', EmpoweringCommunitiesViewSet)
router.register(r'users', UserViewSet)
router.register(r'agents', AgentViewSet, basename='agent')
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'analytics', AdminAnalyticsViewSet, basename='admin-analytics')
router.register(r'hero', HeroViewSet, basename='admin-hero')
router.register(r'cms-settings', CMSSettingsViewSet)
router.register(r'deals', DealViewSet, basename='deal')

# Public ViewSets
public_router = DefaultRouter()
public_router.register(r'agents', PublicAgentViewSet, basename='public-agent')
public_router.register(r'leads', PublicLeadViewSet, basename='public-lead')
public_router.register(r'hero', PublicHeroViewSet, basename='public-hero')

# Agent ViewSets  
agent_router = DefaultRouter()
agent_router.register(r'leads', AgentLeadViewSet, basename='agent-lead')
agent_router.register(r'analytics', AgentAnalyticsViewSet, basename='agent-analytics')


urlpatterns = [
    path('', include(router.urls)),
    path('public/', include(public_router.urls)),
    path('agent/', include(agent_router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('agent/revenue/', AgentRevenueView.as_view(), name='agent-revenue'),
]
