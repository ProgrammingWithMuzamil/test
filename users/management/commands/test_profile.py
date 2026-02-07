from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer

class Command(BaseCommand):
    help = 'Test profile endpoint response'

    def handle(self, *args, **options):
        User = get_user_model()
        
        try:
            user = User.objects.get(email='admin@gmail.com')
            serializer = UserSerializer(user)
            
            self.stdout.write('Profile endpoint response:')
            self.stdout.write(str(serializer.data))
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('User with email admin@gmail.com not found')
            )
