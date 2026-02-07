from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from decimal import Decimal

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('agent', 'Agent'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='agent')
    
    # Agent profile fields
    photo = models.ImageField(upload_to='agents/photos/', null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    profile_visible = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username']  

    def __str__(self):
        return self.email
    
    @property
    def is_admin_role(self):
        """Check if user has admin role"""
        return self.role == 'admin'
    
    @property
    def is_agent_role(self):
        """Check if user has agent role"""
        return self.role == 'agent'
    
    @property
    def is_active_agent(self):
        """Check if agent is active and visible"""
        return self.role == 'agent' and self.status == 'active' and self.profile_visible


class Property(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.CharField(max_length=100)
    img = models.ImageField(upload_to='properties/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Collaboration(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    img = models.ImageField(upload_to='collaborations/', null=True, blank=True) 
    logo = models.ImageField(upload_to='collaborations/logos/', null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Slide(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    img = models.ImageField(upload_to='slides/', null=True, blank=True)  
    points = models.JSONField(default=list)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class YourPerfect(models.Model):
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=100)
    img = models.ImageField(upload_to='yourperfect/', null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class SidebarCard(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField() 
    img = models.ImageField(upload_to='sidebarcard/', null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Damac(models.Model):
    video = models.URLField()  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Video {self.id}"
    


class EmpoweringCommunities(models.Model):
    video = models.URLField()  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"Empowering Community Video {self.id}"


class CMSSettings(models.Model):
    """
    Global CMS settings for controlling section visibility
    """
    heroSection = models.BooleanField(default=True, help_text="Show hero section")
    agentsSection = models.BooleanField(default=True, help_text="Show agents section")
    propertiesSection = models.BooleanField(default=True, help_text="Show properties section")
    leadFormSection = models.BooleanField(default=True, help_text="Show lead form section")
    marketingSection = models.BooleanField(default=True, help_text="Show marketing section")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "CMS Settings"
        verbose_name_plural = "CMS Settings"

    def __str__(self):
        return f"CMS Settings (Updated: {self.updated_at.strftime('%Y-%m-%d')})"

    @classmethod
    def get_settings(cls):
        """Get or create default settings"""
        settings, created = cls.objects.get_or_create(
            id=1,  # Ensure only one row exists
            defaults={
                'heroSection': True,
                'agentsSection': True,
                'propertiesSection': True,
                'leadFormSection': True,
                'marketingSection': True,
            }
        )
        return settings


class Hero(models.Model):
    """
    Hero section model for CMS-controlled hero content
    """
    TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='image')
    heading = models.CharField(max_length=255)
    subheading = models.CharField(max_length=500, null=True, blank=True)
    cta_text = models.CharField(max_length=200, null=True, blank=True)
    cta_link = models.URLField(max_length=500, null=True, blank=True)
    media = models.ImageField(upload_to='hero/', null=True, blank=True)
    video = models.URLField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hero"
        verbose_name_plural = "Heroes"
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.heading} ({self.get_type_display()})"

    def get_type_display(self):
        return dict(self.TYPE_CHOICES).get(self.type, self.type)


class Lead(models.Model):
    """
    Lead model for managing customer inquiries and assignments
    """
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'),
        ('converted', 'Converted'),
        ('closed_lost', 'Closed Lost'),
    ]
    
    
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    source_page = models.CharField(max_length=255, null=True, blank=True, help_text="Page or property slug where lead originated")
    traffic_source = models.CharField(max_length=225, blank=True, null=True)
    
    # UTM Tracking fields
    utm_source = models.CharField(max_length=255, null=True, blank=True, help_text="UTM source parameter")
    utm_medium = models.CharField(max_length=255, null=True, blank=True, help_text="UTM medium parameter")
    utm_campaign = models.CharField(max_length=255, null=True, blank=True, help_text="UTM campaign parameter")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    assigned_agent = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_leads',
        limit_choices_to={'role': 'agent'}
    )
    internal_notes = models.JSONField(default=dict, null=True, blank=True, help_text="Internal notes and activity log")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.email})"

    @property
    def is_assigned(self):
        """Check if lead has an assigned agent"""
        return self.assigned_agent is not None

    @property
    def is_convertible(self):
        """Check if lead can be marked as converted"""
        return self.status in ['in_progress', 'contacted']

    def add_note(self, note, author=None):
        """Add a note to internal notes"""
        if not self.internal_notes:
            self.internal_notes = {}
        
        import datetime
        timestamp = datetime.datetime.now().isoformat()
        self.internal_notes[timestamp] = {
            'note': note,
            'author': author or 'System',
            'timestamp': timestamp
        }
        self.save()

    def can_agent_update_status(self, new_status):
        """Check if agent can update to this status"""
        allowed_transitions = {
            'new': ['new', 'contacted'],  # Can keep as new or move to contacted
            'contacted': ['contacted', 'in_progress'],  # Can keep as contacted or move to in_progress
            'in_progress': ['in_progress'],  # Can only stay in in_progress
        }
        
        # Agents can never set these statuses
        forbidden_statuses = ['converted', 'closed_lost']
        if new_status in forbidden_statuses:
            return False
            
        return new_status in allowed_transitions.get(self.status, [])


class LeadNote(models.Model):
    """
    Lead note model for tracking activity history
    """
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='lead_notes')
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Lead Note"
        verbose_name_plural = "Lead Notes"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Note by {self.user} on {self.lead.name} at {self.created_at}"


class Deal(models.Model):
    """
    Deal model for tracking revenue and commission for converted leads
    """
    CURRENCY_CHOICES = [
        ('AED', 'UAE Dirham'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
    ]
    
    lead = models.OneToOneField(
        Lead, 
        on_delete=models.CASCADE, 
        related_name='deal',
        help_text="The converted lead this deal is associated with"
    )
    revenue_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        help_text="Total revenue amount from this deal"
    )
    currency = models.CharField(
        max_length=3, 
        choices=CURRENCY_CHOICES, 
        default='AED',
        help_text="Currency for the revenue amount"
    )
    closed_date = models.DateField(
        help_text="Date when the deal was closed"
    )
    commission_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Commission rate percentage (e.g., 5.00 for 5%)"
    )
    commission_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Calculated commission amount"
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_deals',
        limit_choices_to={'role': 'admin'},
        help_text="Admin user who created this deal"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Deal"
        verbose_name_plural = "Deals"
        ordering = ['-closed_date']

    def __str__(self):
        return f"Deal for {self.lead.name} - {self.revenue_amount} {self.currency}"

    def clean(self):
        """Validate deal constraints"""
        if self.lead.status != 'converted':
            raise ValidationError("Deal can only be created for converted leads")
        
        if self.commission_rate is not None and (self.commission_rate < 0 or self.commission_rate > 100):
            raise ValidationError("Commission rate must be between 0 and 100")

    def save(self, *args, **kwargs):
        self.clean()
        
        # Auto-calculate commission amount if rate is provided
        if self.commission_rate is not None and self.commission_amount is None:
            self.commission_amount = (self.revenue_amount * Decimal(str(self.commission_rate))) / Decimal('100')
        elif self.commission_rate is None:
            self.commission_amount = None
            
        super().save(*args, **kwargs)

    @property
    def commission_percentage(self):
        """Return commission rate as percentage string"""
        if self.commission_rate is not None:
            return f"{self.commission_rate}%"
        return "Not set"