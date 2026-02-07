from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Force update user role to admin and clear session'

    def handle(self, *args, **options):
        User = get_user_model()
        
        try:
            user = User.objects.get(email='admin@gmail.com')
            
            # Force update all admin-related fields
            user.role = 'admin'
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            
            self.stdout.write(self.style.SUCCESS('✅ User role force updated to admin'))
            self.stdout.write(f'✅ Email: {user.email}')
            self.stdout.write(f'✅ Role: {user.role}')
            self.stdout.write(f'✅ Is Staff: {user.is_staff}')
            self.stdout.write(f'✅ Is Superuser: {user.is_superuser}')
            
            # Test the serializer response
            from users.serializers import UserSerializer
            serializer = UserSerializer(user)
            self.stdout.write(f'✅ Serializer Response: {serializer.data}')
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('❌ User with email admin@gmail.com not found')
            )
