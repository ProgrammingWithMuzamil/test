from rest_framework import serializers
from .models import CustomUser, Property, Collaboration, Slide, YourPerfect, SidebarCard, Damac, EmpoweringCommunities, CMSSettings, Lead, LeadNote, Hero, Deal
from django.conf import settings

class PropertySerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()
    class Meta:
        model = Property
        fields = '__all__'

    def get_img_url(self, obj):
        if obj.img:
            return f"{settings.BACKEND_URL}{obj.img.url}"
        else:
            return None


class CollaborationSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()
    logo_url = serializers.SerializerMethodField()
    class Meta:
        model = Collaboration
        fields = '__all__'

    def get_img_url(self, obj):
        if obj.img:
            return f"{settings.BACKEND_URL}{obj.img.url}"
        return None
    
    def get_logo_url(self, obj):
        if obj.logo:
            return f"{settings.BACKEND_URL}{obj.logo.url}"
        return None




class SlideSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()
    class Meta:
        model = Slide
        fields = '__all__'
    def get_img_url(self, obj):
        if obj.img:
            return f"{settings.BACKEND_URL}{obj.img.url}"
        return None



class YourPerfectSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()
    class Meta:
        model = YourPerfect
        fields = '__all__'

    def get_img_url(self, obj):
        if obj.img:
            return f"{settings.BACKEND_URL}{obj.img.url}"
        return None



class SidebarCardSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()
    class Meta:
        model = SidebarCard
        fields = '__all__'

    def get_img_url(self, obj):
        if obj.img:
            return f"{settings.BACKEND_URL}{obj.img.url}"
        return None


class DamacSerializer(serializers.ModelSerializer):
    class Meta:
        model = Damac
        fields = '__all__'


class EmpoweringCommunitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpoweringCommunities
        fields = '__all__'  



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'is_superuser', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class CMSSettingsSerializer(serializers.ModelSerializer):
    """Serializer for CMS Settings model"""
    
    class Meta:
        model = CMSSettings
        fields = '__all__'


class AgentSerializer(serializers.ModelSerializer):
    """Serializer for Agent model (CustomUser with agent role)"""
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'role',
            'photo', 'photo_url', 'title', 'phone', 'bio', 'status', 'profile_visible'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'role': {'default': 'agent'}
        }
    
    def get_photo_url(self, obj):
        """Get full photo URL"""
        if obj.photo:
            from django.conf import settings
            return f"{settings.BACKEND_URL}{obj.photo.url}"
        return None
    
    def validate_role(self, value):
        """Ensure role is always 'agent' for this serializer"""
        if value != 'agent':
            raise serializers.ValidationError("Only 'agent' role is allowed for this serializer")
        return value
    
    def create(self, validated_data):
        """Create agent user with password"""
        password = validated_data.pop('password', None)
        validated_data['role'] = 'agent'  # Force role to agent
        
        user = CustomUser.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class LeadNoteSerializer(serializers.ModelSerializer):
    """Serializer for Lead notes"""
    user_name = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()
    
    class Meta:
        model = LeadNote
        fields = ['id', 'note', 'user', 'user_name', 'user_email', 'created_at']
        read_only_fields = ['user', 'created_at']
    
    def get_user_name(self, obj):
        """Get user name"""
        if obj.user:
            return obj.user.get_full_name() or obj.user.username
        return 'System'
    
    def get_user_email(self, obj):
        """Get user email"""
        if obj.user:
            return obj.user.email
        return None


class LeadSerializer(serializers.ModelSerializer):
    """Serializer for Lead model (admin full access)"""
    assigned_agent_name = serializers.SerializerMethodField()
    assigned_agent_email = serializers.SerializerMethodField()
    notes_history = LeadNoteSerializer(source='notes', many=True, read_only=True)
    
    class Meta:
        model = Lead
        fields = [
            'id', 'name', 'email', 'phone', 'source_page', 'traffic_source',
            'utm_source', 'utm_medium', 'utm_campaign',
            'status', 'assigned_agent', 'assigned_agent_name', 'assigned_agent_email',
            'internal_notes', 'notes_history', 'created_at', 'updated_at'
        ]
    
    def get_assigned_agent_name(self, obj):
        """Get assigned agent name"""
        if obj.assigned_agent:
            return obj.assigned_agent.get_full_name() or obj.assigned_agent.username
        return None
    
    def get_assigned_agent_email(self, obj):
        """Get assigned agent email"""
        if obj.assigned_agent:
            return obj.assigned_agent.email
        return None
    
    def validate_assigned_agent(self, value):
        """Validate that assigned agent has agent role"""
        if value and value.role != 'agent':
            raise serializers.ValidationError("Assigned user must have agent role")
        return value


class AgentLeadSerializer(serializers.ModelSerializer):
    """Serializer for Lead model (agent restricted access)"""
    assigned_agent_name = serializers.SerializerMethodField()
    notes_history = LeadNoteSerializer(source='notes', many=True, read_only=True)
    
    class Meta:
        model = Lead
        fields = [
            'id', 'name', 'email', 'phone', 'source_page', 'traffic_source',
            'utm_source', 'utm_medium', 'utm_campaign',
            'status', 'assigned_agent_name', 'internal_notes', 'notes_history', 'created_at', 'updated_at'
        ]
        read_only_fields = ['assigned_agent', 'name', 'email', 'phone', 'source_page', 'traffic_source', 'utm_source', 'utm_medium', 'utm_campaign']
    
    def get_assigned_agent_name(self, obj):
        """Get assigned agent name"""
        if obj.assigned_agent:
            return obj.assigned_agent.get_full_name() or obj.assigned_agent.username
        return None
    
    def validate_status(self, value):
        """Validate status transitions for agents"""
        # Get current status if updating
        if self.instance:
            current_status = self.instance.status
            if not self.instance.can_agent_update_status(value):
                raise serializers.ValidationError(
                    f"Agents cannot change status from '{current_status}' to '{value}'"
                )
        return value
    
    def validate(self, attrs):
        """Additional validation for agent updates"""
        # Agents cannot reassign leads
        if 'assigned_agent' in attrs and attrs['assigned_agent'] != self.instance.assigned_agent:
            raise serializers.ValidationError("Agents cannot reassign leads to other agents")
        return attrs


class HeroSerializer(serializers.ModelSerializer):
    """Serializer for Hero model (admin full access)"""
    media_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Hero
        fields = [
            'id', 'type', 'heading', 'subheading', 'cta_text', 'cta_link',
            'media', 'media_url', 'video', 'is_active', 'created_at', 'updated_at'
        ]
    
    def get_media_url(self, obj):
        """Get full media URL"""
        if obj.media:
            from django.conf import settings
            return f"{settings.BACKEND_URL}{obj.media.url}"
        return None


class PublicHeroSerializer(serializers.ModelSerializer):
    """Serializer for Hero model (public read-only)"""
    media_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Hero
        fields = [
            'type', 'heading', 'subheading', 'cta_text', 'cta_link',
            'media_url', 'video'
        ]
        read_only_fields = ['type', 'heading', 'subheading', 'cta_text', 'cta_link', 'media_url', 'video']
    
    def get_media_url(self, obj):
        """Get full media URL"""
        if obj.media:
            from django.conf import settings
            return f"{settings.BACKEND_URL}{obj.media.url}"
        return None


class PublicLeadSerializer(serializers.ModelSerializer):
    """Serializer for public lead creation"""
    
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'source_page', 'traffic_source', 'utm_source', 'utm_medium', 'utm_campaign']
        extra_kwargs = {
            'source_page': {'required': False, 'allow_null': True},
            'traffic_source': {'default': 'organic'},
            'utm_source': {'required': False, 'allow_null': True},
            'utm_medium': {'required': False, 'allow_null': True},
            'utm_campaign': {'required': False, 'allow_null': True}
        }


class DealSerializer(serializers.ModelSerializer):
    """Serializer for Deal model (admin only)"""
    lead_name = serializers.SerializerMethodField()
    lead_email = serializers.SerializerMethodField()
    agent_name = serializers.SerializerMethodField()
    agent_email = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    commission_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Deal
        fields = [
            'id', 'lead', 'lead_name', 'lead_email', 'revenue_amount', 'currency',
            'closed_date', 'commission_rate', 'commission_amount', 'commission_percentage',
            'created_by', 'created_by_name', 'agent_name', 'agent_email', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
    def get_lead_name(self, obj):
        """Get lead name"""
        return obj.lead.name
    
    def get_lead_email(self, obj):
        """Get lead email"""
        return obj.lead.email
    
    def get_agent_name(self, obj):
        """Get assigned agent name"""
        if obj.lead.assigned_agent:
            return obj.lead.assigned_agent.get_full_name() or obj.lead.assigned_agent.username
        return None
    
    def get_agent_email(self, obj):
        """Get assigned agent email"""
        if obj.lead.assigned_agent:
            return obj.lead.assigned_agent.email
        return None
    
    def get_created_by_name(self, obj):
        """Get creator name"""
        if obj.created_by:
            return obj.created_by.get_full_name() or obj.created_by.username
        return None
    
    def validate(self, attrs):
        """Validate deal constraints"""
        # Check if lead is converted when creating new deal
        if not self.instance:  # Creating new deal
            lead = attrs.get('lead')
            if lead and lead.status != 'converted':
                raise serializers.ValidationError(
                    {"lead": "Deal can only be created for converted leads"}
                )
        
        # Validate commission rate
        commission_rate = attrs.get('commission_rate')
        if commission_rate is not None and (commission_rate < 0 or commission_rate > 100):
            raise serializers.ValidationError(
                {"commission_rate": "Commission rate must be between 0 and 100"}
            )
        
        return attrs
    
    def create(self, validated_data):
        """Create deal with current admin as creator"""
        request = self.context.get('request')
        if request and request.user:
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class AgentDealSerializer(serializers.ModelSerializer):
    """Serializer for Deal model (agent read-only access)"""
    lead_name = serializers.SerializerMethodField()
    lead_email = serializers.SerializerMethodField()
    commission_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Deal
        fields = [
            'id', 'lead', 'lead_name', 'lead_email', 'revenue_amount', 'currency',
            'closed_date', 'commission_rate', 'commission_amount', 'commission_percentage',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'lead', 'lead_name', 'lead_email', 'revenue_amount', 'currency', 'closed_date', 'commission_rate', 'commission_amount', 'commission_percentage', 'created_at', 'updated_at']
    
    def get_lead_name(self, obj):
        """Get lead name"""
        return obj.lead.name
    
    def get_lead_email(self, obj):
        """Get lead email"""
        return obj.lead.email


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for user self-profile updates"""
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    profile_image = serializers.ImageField(source='photo', required=False, allow_null=True)
    profile_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'title', 'phone', 'bio', 'profile_image', 'profile_image_url', 'password']
        read_only_fields = ['id', 'email']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'title': {'required': False},
            'phone': {'required': False},
            'bio': {'required': False},
        }
    
    def get_profile_image_url(self, obj):
        """Get full profile image URL"""
        if obj.photo:
            from django.conf import settings
            return f"{settings.BACKEND_URL}{obj.photo.url}"
        return None
    
    def validate_password(self, value):
        """Validate password - ignore if empty string"""
        if value == '':
            return None
        return value
    
    def update(self, instance, validated_data):
        """Update user profile with secure password handling"""
        password = validated_data.pop('password', None)
        photo = validated_data.pop('photo', None)
        
        # Update regular fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Handle password update securely
        if password:
            instance.set_password(password)
        
        # Handle profile image
        if photo is not None:
            instance.photo = photo
        
        instance.save()
        return instance


class AgentRevenueSerializer(serializers.Serializer):
    """Serializer for agent revenue statistics"""
    total_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_commission = serializers.DecimalField(max_digits=15, decimal_places=2)
    converted_leads_count = serializers.IntegerField()
    revenue_by_month = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        allow_null=True
    )
    recent_deals = AgentDealSerializer(many=True, required=False, allow_null=True)
