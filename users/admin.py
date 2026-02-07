from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import (
    Property, Collaboration, Slide, YourPerfect, SidebarCard, Damac, 
    EmpoweringCommunities, CMSSettings, Hero, Lead
)

User = get_user_model()

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'img', 'created_at', 'updated_at')
    search_fields = ('title', 'location')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'location', 'price', 'img')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Collaboration)
class CollaborationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'desc')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'desc')
        }),
        ('Images', {
            'fields': ('img', 'logo')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
 
@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'created_at', 'updated_at')
    search_fields = ('title', 'location')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'location')
        }),
        ('Images', {
            'fields': ('img',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(YourPerfect)
class YourPerfectAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'updated_at')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'price')
        }),
        ('Images', {
            'fields': ('img',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(SidebarCard)
class SidebarCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'desc')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'desc')
        }),
        ('Images', {
            'fields': ('img',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Damac)
class DamacAdmin(admin.ModelAdmin):
    list_display = ('video', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Video Content', {
            'fields': ('video',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
 
@admin.register(EmpoweringCommunities)
class EmpoweringCommunitiesAdmin(admin.ModelAdmin):
    list_display = ('video', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Video Content', {
            'fields': ('video',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(CMSSettings)
class CMSSettingsAdmin(admin.ModelAdmin):
    list_display = ('heroSection', 'agentsSection', 'propertiesSection', 'leadFormSection', 'marketingSection', 'updated_at')
    list_filter = ('heroSection', 'agentsSection', 'propertiesSection', 'leadFormSection', 'marketingSection')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Section Visibility', {
            'fields': ('heroSection', 'agentsSection', 'propertiesSection', 'leadFormSection', 'marketingSection')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Prevent creation of multiple CMS settings instances
        return not CMSSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of CMS settings
        return False

@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('heading', 'type', 'is_active', 'created_at', 'updated_at')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'status', 'is_active', 'date_joined')
    list_filter = ('role', 'status', 'is_active', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'username')
        }),
        ('Agent Profile', {
            'fields': ('title', 'phone', 'bio', 'photo', 'profile_visible')
        }),
        ('Status', {
            'fields': ('role', 'status', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Permissions', {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'status', 'assigned_agent', 'created_at', 'updated_at')
    list_filter = ('status', 'assigned_agent', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Lead Details', {
            'fields': ('message', 'property_interest', 'budget', 'preferred_contact')
        }),
        ('Assignment', {
            'fields': ('assigned_agent', 'status')
        }),
        ('Internal Notes', {
            'fields': ('internal_notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
