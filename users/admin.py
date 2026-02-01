from django.contrib import admin
from .models import Property, Collaboration, Slide, YourPerfect, SidebarCard, Damac, EmpoweringCommunities

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'created_at', 'updated_at')
    search_fields = ('title', 'location')

@admin.register(Collaboration)
class CollaborationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)
 
@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'created_at', 'updated_at')
    search_fields = ('title', 'location')

@admin.register(YourPerfect)
class YourPerfectAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'updated_at')
    search_fields = ('title',)

@admin.register(SidebarCard)
class SidebarCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')

@admin.register(Damac)
class DamacAdmin(admin.ModelAdmin):
    list_display = ('video', 'created_at', 'updated_at')
 
@admin.register(EmpoweringCommunities)
class EmpoweringCommunitiesAdmin(admin.ModelAdmin):
    list_display = ('video', 'created_at', 'updated_at')
