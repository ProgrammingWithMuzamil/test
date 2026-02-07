from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q, F, Expression
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from .serializers import (
    LoginSerializer, UserSerializer, PropertySerializer, CollaborationSerializer, 
    SlideSerializer, YourPerfectSerializer, SidebarCardSerializer, DamacSerializer,
    EmpoweringCommunitiesSerializer, CMSSettingsSerializer, AgentSerializer,
    LeadSerializer, AgentLeadSerializer, PublicLeadSerializer, HeroSerializer,
    PublicHeroSerializer, LeadNoteSerializer, DealSerializer, AgentDealSerializer, 
    AgentRevenueSerializer, ProfileUpdateSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdminOrReadOnly, IsAdminOrSelf, IsAdminUser, IsAdminRole, IsAgentRole, IsAdminOrAgentRole, IsAdminOnly
from .models import CustomUser, Property, Collaboration, Slide, YourPerfect, SidebarCard, Damac, EmpoweringCommunities, CMSSettings, Lead, LeadNote, Hero, Deal


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
                        "role": user.role,  # Use role field from CustomUser
                        "is_admin": user.is_admin_role,  # Helper property
                        "is_agent": user.is_agent_role,  # Helper property
                    },
                    "token": access_token
                }

                return Response(user_data, status=status.HTTP_200_OK)

            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication for profile access

    def get(self, request):
        """Get current user profile"""
        user = request.user
        user_data = {
            "id": user.id,
            "email": user.email,
            "title": user.title,
            "phone": user.phone,
            "bio": user.bio,
            "role": user.role,
            "is_admin": user.is_admin_role,
            "is_agent": user.is_agent_role,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "profile_image_url": None,
        }
        
        # Add profile image URL if exists
        if user.photo:
            user_data["profile_image_url"] = f"{settings.BACKEND_URL}{user.photo.url}"
            
        return Response({"user": user_data})
    
    def patch(self, request):
        """Update current user profile"""
        user = request.user
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            updated_user = serializer.save()
            
            # Return updated user data
            user_data = {
                "id": updated_user.id,
                "email": updated_user.email,
                "title": updated_user.title,
                "phone": updated_user.phone,
                "bio": updated_user.bio,
                "role": updated_user.role,
                "is_admin": updated_user.is_admin_role,
                "is_agent": updated_user.is_agent_role,
                "is_staff": updated_user.is_staff,
                "is_superuser": updated_user.is_superuser,
                "profile_image_url": None,
            }
            
            # Add profile image URL if exists
            if updated_user.photo:
                user_data["profile_image_url"] = f"{settings.BACKEND_URL}{updated_user.photo.url}"
                
            return Response({"user": user_data}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


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
            permission_classes = [IsAdminOnly]  # Only admin can create users
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOnly]  # Only admin can modify users
        elif self.action == 'list':
            permission_classes = [IsAdminOnly]  # Only admin can list users
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


class CMSSettingsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CMS Settings with custom permissions and singleton behavior
    """
    serializer_class = CMSSettingsSerializer
    queryset = CMSSettings.objects.all()  # Required for router registration
    
    def get_permissions(self):
        """
        GET requests are public (for frontend visibility)
        PUT/PATCH/DELETE are admin-only
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminOnly]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Ensure only one CMS settings instance exists
        """
        return CMSSettings.objects.filter(id=1)
    
    def get_object(self):
        """
        Always return the single CMS settings instance
        """
        return CMSSettings.get_settings()
    
    def list(self, request):
        """
        Return the single CMS settings instance
        """
        settings = CMSSettings.get_settings()
        serializer = self.get_serializer(settings)
        return Response(serializer.data)
    
    def create(self, request):
        """
        Prevent creation - always update the existing instance
        """
        return Response({'detail': 'Creation not allowed. Use PUT to update settings.'}, 
                       status=status.HTTP_405_METHOD_NOT_ALLOWED)


class AgentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Agent management (admin-only)
    """
    serializer_class = AgentSerializer
    permission_classes = [IsAdminOnly]
    queryset = CustomUser.objects.filter(role='agent')
    
    def get_queryset(self):
        """Return only users with agent role"""
        return CustomUser.objects.filter(role='agent')
    
    def perform_destroy(self, instance):
        """Soft delete by setting status to inactive"""
        instance.status = 'inactive'
        instance.profile_visible = False
        instance.save()


class PublicAgentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public ViewSet for displaying active agents on website
    """
    serializer_class = AgentSerializer
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.filter(role='agent', status='active', profile_visible=True)
    
    def get_queryset(self):
        """Return only active, visible agents if CMS allows"""
        # Check if agents section is enabled in CMS settings
        cms_settings = CMSSettings.get_settings()
        
        if not cms_settings.agentsSection:
            return CustomUser.objects.none()
        
        return CustomUser.objects.filter(
            role='agent',
            status='active',
            profile_visible=True
        )


class LeadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Lead management (admin-only)
    """
    serializer_class = LeadSerializer
    permission_classes = [IsAdminOnly]
    queryset = Lead.objects.all()
    
    def get_queryset(self):
        """Filter leads by status, agent, and traffic source if provided"""
        queryset = Lead.objects.all()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by agent
        agent_filter = self.request.query_params.get('agent')
        if agent_filter:
            queryset = queryset.filter(assigned_agent_id=agent_filter)
        
        # Filter by traffic source
        traffic_source_filter = self.request.query_params.get('traffic_source')
        if traffic_source_filter:
            queryset = queryset.filter(traffic_source=traffic_source_filter)
        
        # Filter by UTM campaign
        utm_campaign_filter = self.request.query_params.get('utm_campaign')
        if utm_campaign_filter:
            queryset = queryset.filter(utm_campaign=utm_campaign_filter)
        
        # Filter by source page
        source_page_filter = self.request.query_params.get('source_page')
        if source_page_filter:
            queryset = queryset.filter(source_page__icontains=source_page_filter)
        
        return queryset
    
    def perform_create(self, serializer):
        """Handle lead creation with CMS check"""
        # Check if lead form is enabled in CMS settings
        cms_settings = CMSSettings.get_settings()
        
        if not cms_settings.leadFormSection:
            return Response(
                {'detail': 'Lead form is currently disabled'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create lead
        lead = serializer.save()
        return Response(LeadSerializer(lead).data, status=status.HTTP_201_CREATED)


class AgentLeadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for agents to manage their assigned leads
    """
    serializer_class = AgentLeadSerializer
    permission_classes = [IsAgentRole]
    
    def get_queryset(self):
        """Return only leads assigned to current agent with filtering"""
        queryset = Lead.objects.filter(assigned_agent=self.request.user)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by search (name, email, phone)
        search_filter = self.request.query_params.get('search')
        if search_filter:
            queryset = queryset.filter(
                Q(name__icontains=search_filter) |
                Q(email__icontains=search_filter) |
                Q(phone__icontains=search_filter)
            )
        
        return queryset
    
    def update(self, request, *args, **kwargs):
        """Handle lead updates with status transition validation and note creation"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            # Handle status change
            if 'status' in request.data and request.data['status'] != instance.status:
                note_text = f"Status changed from '{instance.status}' to '{request.data['status']}'"
                LeadNote.objects.create(
                    lead=instance,
                    user=request.user,
                    note=note_text
                )
            
            # Handle activity note
            if 'activity_note' in request.data and request.data['activity_note']:
                LeadNote.objects.create(
                    lead=instance,
                    user=request.user,
                    note=request.data['activity_note']
                )
                # Remove activity_note from the data before saving
                request.data.pop('activity_note')
            
            self.perform_update(serializer)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        """Agents cannot create leads"""
        return Response(
            {'detail': 'Agents cannot create leads'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    def perform_destroy(self, instance):
        """Agents cannot delete leads"""
        return Response(
            {'detail': 'Agents cannot delete leads'},
            status=status.HTTP_403_FORBIDDEN
        )


class PublicLeadViewSet(viewsets.GenericViewSet):
    """
    Public ViewSet for lead creation from website forms
    """
    serializer_class = PublicLeadSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        """Create lead from public form"""
        # Check if lead form is enabled in CMS settings
        cms_settings = CMSSettings.get_settings()
        
        if not cms_settings.leadFormSection:
            return Response(
                {'detail': 'Lead form is currently disabled'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            lead = serializer.save()
            return Response(
                {'message': 'Lead submitted successfully', 'lead_id': lead.id},
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminAnalyticsViewSet(viewsets.ViewSet):
    """
    ViewSet for admin analytics and performance metrics
    """
    permission_classes = [IsAdminOnly]
    
    def list(self, request):
        """Get comprehensive analytics overview"""
        try:
            from datetime import datetime
            from django.utils.timezone import now
            
            # Get filters
            date_from = request.query_params.get('date_from')
            date_to = request.query_params.get('date_to')
            agent_id = request.query_params.get('agent_id')
            
            # Base queryset
            queryset = Lead.objects.all()
            
            # Apply date filters with proper parsing
            if date_from:
                try:
                    date_from_parsed = datetime.strptime(date_from, '%Y-%m-%d').date()
                    queryset = queryset.filter(created_at__date__gte=date_from_parsed)
                except ValueError:
                    pass  # Invalid date format, ignore filter
            
            if date_to:
                try:
                    date_to_parsed = datetime.strptime(date_to, '%Y-%m-%d').date()
                    queryset = queryset.filter(created_at__date__lte=date_to_parsed)
                except ValueError:
                    pass  # Invalid date format, ignore filter
            
            # Apply agent filter
            if agent_id and agent_id.isdigit():
                queryset = queryset.filter(assigned_agent_id=int(agent_id))
            
            # Overall stats
            total_leads = queryset.count()
            converted_leads = queryset.filter(status='converted').count()
            closed_lost_leads = queryset.filter(status='closed_lost').count()
            
            # Conversion rate calculation
            conversion_rate = 0
            if total_leads > 0:
                conversion_rate = (converted_leads / total_leads) * 100
            
            # Status breakdown
            status_breakdown = queryset.values('status').annotate(count=Count('id')).order_by('status')
            
            # Traffic breakdown
            traffic_breakdown = queryset.values('traffic_source').annotate(count=Count('id')).order_by('-count')
            
            # Agent performance
            agent_stats = []
            agents = CustomUser.objects.filter(role='agent')
            for agent in agents:
                agent_leads = queryset.filter(assigned_agent=agent)
                agent_converted = agent_leads.filter(status='converted').count()
                agent_total = agent_leads.count()
                agent_rate = (agent_converted / agent_total * 100) if agent_total > 0 else 0
                
                agent_stats.append({
                    'agent_id': agent.id,
                    'agent_name': agent.get_full_name() or agent.email,
                    'total_leads': agent_total,
                    'converted_leads': agent_converted,
                    'conversion_rate': round(agent_rate, 2),
                })
            
            # Recent leads (last 30 days)
            recent_date = now() - timedelta(days=30)
            recent_leads = Lead.objects.filter(created_at__gte=recent_date).count()
            
            data = {
                'overview': {
                    'total_leads': total_leads,
                    'converted_leads': converted_leads,
                    'closed_lost_leads': closed_lost_leads,
                    'conversion_rate': round(conversion_rate, 2),
                    'recent_leads': recent_leads,
                },
                'status_breakdown': list(status_breakdown),
                'traffic_breakdown': list(traffic_breakdown),
                'agent_performance': agent_stats,
            }
            
            return Response(data)
            
        except Exception as e:
            return Response(
                {'error': f'Analytics calculation failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


from django.db.models import Count, Q
from collections import defaultdict

class AgentAnalyticsViewSet(viewsets.ViewSet):
    """
    ViewSet for agent-specific analytics
    """
    permission_classes = [IsAgentRole]
    
    def list(self, request):
        """Get analytics for current agent"""
        try:
            from datetime import datetime
            from django.utils.timezone import now
            
            agent = request.user
            
            date_from = request.query_params.get('date_from')
            date_to   = request.query_params.get('date_to')
            
            queryset = Lead.objects.filter(assigned_agent=agent)
            
            if date_from:
                try:
                    date_from_parsed = datetime.strptime(date_from, '%Y-%m-%d').date()
                    queryset = queryset.filter(created_at__date__gte=date_from_parsed)
                except ValueError:
                    pass
            
            if date_to:
                try:
                    date_to_parsed = datetime.strptime(date_to, '%Y-%m-%d').date()
                    queryset = queryset.filter(created_at__date__lte=date_to_parsed)
                except ValueError:
                    pass
            
            total_leads         = queryset.count()
            new_leads           = queryset.filter(status='new').count()
            contacted_leads     = queryset.filter(status='contacted').count()
            in_progress_leads   = queryset.filter(status='in_progress').count()
            converted_leads     = queryset.filter(status='converted').count()
            closed_lost_leads   = queryset.filter(status='closed_lost').count()
            
            conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0
            
            STATUS_ORDER = ['new', 'contacted', 'in_progress', 'converted', 'closed_lost']
            STATUS_LABELS = {
                'new': 'New',
                'contacted': 'Contacted',
                'in_progress': 'In Progress',
                'converted': 'Converted',
                'closed_lost': 'Closed Lost',
            }
            
            real_counts = (
                queryset
                .values('status')
                .annotate(count=Count('id'))
                .order_by('status')
            )
            
            count_dict = {item['status']: item['count'] for item in real_counts}
            
            status_breakdown = [
                {
                    'status': s,
                    'label': STATUS_LABELS[s],
                    'count': count_dict.get(s, 0)
                }
                for s in STATUS_ORDER
            ]
            
            recent_date = now() - timedelta(days=7)
            recent_activity = (
                queryset
                .filter(updated_at__gte=recent_date)   
                .order_by('-updated_at')
                .values('id', 'name', 'email', 'status', 'updated_at', 'internal_notes')[:5]
            )
            
            data = {
                'overview': {
                    'total_leads': total_leads,
                    'new_leads': new_leads,
                    'contacted_leads': contacted_leads,
                    'in_progress_leads': in_progress_leads,
                    'converted_leads': converted_leads,
                    'closed_lost_leads': closed_lost_leads,
                    'conversion_rate': round(conversion_rate, 2),
                },
                'status_breakdown': status_breakdown,
                'recent_activity': list(recent_activity),
            }
            
            return Response(data)
            
        except Exception as e:
            return Response(
                {'error': f'Agent analytics calculation failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class HeroViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Hero model (admin only)
    """
    serializer_class = HeroSerializer
    permission_classes = [IsAdminOnly]
    queryset = Hero.objects.all()
    
    def get_queryset(self):
        """Return all heroes, ordered by updated_at"""
        return Hero.objects.all().order_by('-updated_at')
    
    def create(self, request, *args, **kwargs):
        """Create new hero and ensure only one is active"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            hero = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """Update hero - save method handles single active hero logic"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            hero = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicHeroViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Hero model (public read-only)
    """
    serializer_class = PublicHeroSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        """Return only active hero if CMS hero section is enabled"""
        cms_settings = CMSSettings.get_settings()
        if not cms_settings.heroSection:
            return Hero.objects.none()
        
        return Hero.objects.filter(is_active=True).order_by('-updated_at')
    
    def list(self, request, *args, **kwargs):
        """Return single active hero or empty"""
        queryset = self.get_queryset()
        hero = queryset.first()  # Get only the most recent active hero
        
        if hero:
            serializer = self.get_serializer(hero)
            return Response(serializer.data)
        
        return Response({'detail': 'No active hero found'}, status=status.HTTP_404_NOT_FOUND)


class DealViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Deal model (admin only)
    """
    serializer_class = DealSerializer
    permission_classes = [IsAdminOnly]
    queryset = Deal.objects.all()
    
    def get_queryset(self):
        """Filter deals by agent or date if requested"""
        queryset = Deal.objects.select_related('lead', 'lead__assigned_agent', 'created_by').all()
        
        # Filter by agent
        agent_id = self.request.query_params.get('agent_id')
        if agent_id:
            queryset = queryset.filter(lead__assigned_agent_id=agent_id)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(closed_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(closed_date__lte=end_date)
        
        return queryset.order_by('-closed_date')
    
    def create(self, request, *args, **kwargs):
        """Create new deal"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            deal = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """Update deal"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            deal = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """Delete deal"""
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AgentRevenueView(APIView):
    """
    API view for agents to get their personal revenue statistics
    """
    permission_classes = [IsAuthenticated, IsAgentRole]
    
    def get(self, request):
        """Get agent's revenue statistics"""
        try:
            agent = request.user
            
            # Get all deals for this agent's converted leads
            agent_deals = Deal.objects.filter(
                lead__assigned_agent=agent
            ).select_related('lead').order_by('-closed_date')
            
            # Calculate totals
            total_revenue = sum(deal.revenue_amount for deal in agent_deals)
            total_commission = sum(deal.commission_amount or 0 for deal in agent_deals)
            converted_leads_count = agent_deals.count()
            
            # Calculate revenue by month (last 12 months)
            from django.db.models import Sum
            from django.utils import timezone
            from datetime import datetime
            
            revenue_by_month = []
            current_date = timezone.now()
            
            for i in range(12):
                month_start = current_date.replace(day=1) - timezone.timedelta(days=30*i)
                month_end = (month_start + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(days=1)
                
                month_revenue = agent_deals.filter(
                    closed_date__gte=month_start,
                    closed_date__lte=month_end
                ).aggregate(
                    total=Sum('revenue_amount'),
                    commission=Sum('commission_amount'),
                    count=Count('id')
                )
                
                revenue_by_month.append({
                    'month': month_start.strftime('%Y-%m'),
                    'revenue': month_revenue['total'] or 0,
                    'commission': month_revenue['commission'] or 0,
                    'deals_count': month_revenue['count'] or 0
                })
            
            # Get recent deals (last 10)
            recent_deals = agent_deals[:10]
            
            data = {
                'total_revenue': total_revenue,
                'total_commission': total_commission,
                'converted_leads_count': converted_leads_count,
                'revenue_by_month': list(reversed(revenue_by_month)),  # Most recent first
                'recent_deals': recent_deals
            }
            
            serializer = AgentRevenueSerializer(data)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to calculate revenue statistics: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
