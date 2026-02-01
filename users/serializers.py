from rest_framework import serializers
from .models import *
from django.conf import settings

class PropertySerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    class Meta:
        model = Property
        fields = '__all__'

    def get_img(self, obj):
        if obj.img:
            return f"{settings.BACKEND_URL}{obj.img.url}"
        return None


class CollaborationSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()
    class Meta:
        model = Collaboration
        fields = '__all__'

    def get_img(self, obj):
        if obj.img:
            return f"{settings.BACKEND_URL}{obj.img.url}"
        return None
    
    def get_logo(self, obj):
        if obj.logo:
            return f"{settings.BACKEND_URL}{obj.logo.url}"
        return None




class SlideSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    class Meta:
        model = Slide
        fields = '__all__'
    def get_img(self, obj):
        if obj.img:
            return f"{settings.BACKEND_URL}{obj.img.url}"
        return None



class YourPerfectSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    class Meta:
        model = YourPerfect
        fields = '__all__'

    def get_img(self, obj):
        if obj.img:
            return f"{settings.BACKEND_URL}{obj.img.url}"
        return None



class SidebarCardSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    class Meta:
        model = SidebarCard
        fields = '__all__'

    def get_img(self, obj):
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
