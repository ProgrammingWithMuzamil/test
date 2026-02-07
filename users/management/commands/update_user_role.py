from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Update user role to admin'

    def handle(self, *args, **options):
        User = get_user_model()
        
        try:
            # Get the user with email admin@gmail.com
            user = User.objects.get(email='admin@gmail.com')
            
            # Update role to admin and set staff status
            user.role = 'admin'
            user.is_staff = True
            user.is_superuser = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated {user.email} to admin role')
            )
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('User with email admin@gmail.com not found')
            )
