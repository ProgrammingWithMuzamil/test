from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.test import Client
import json

class Command(BaseCommand):
    help = 'Test login endpoint response'

    def handle(self, *args, **options):
        User = get_user_model()
        client = Client()
        
        try:
            # Test login endpoint
            response = client.post('/api/login/', {
                'email': 'admin@gmail.com',
                'password': 'admin123'  # Assuming this is the password
            }, content_type='application/json')
            
            self.stdout.write('Login endpoint status:', response.status_code)
            self.stdout.write('Login response data:')
            self.stdout.write(json.dumps(response.data, indent=2))
            
            # Test profile endpoint
            if response.status_code == 200 and 'token' in response.data:
                token = response.data['token']
                profile_response = client.get('/api/profile/', 
                    HTTP_AUTHORIZATION=f'Bearer {token}',
                    content_type='application/json'
                )
                self.stdout.write('\nProfile endpoint status:', profile_response.status_code)
                self.stdout.write('Profile response data:')
                self.stdout.write(json.dumps(profile_response.data, indent=2))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
