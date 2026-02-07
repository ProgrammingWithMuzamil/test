from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a test agent account'

    def handle(self, *args, **options):
        User = get_user_model()
        
        try:
            # Check if test agent already exists
            if User.objects.filter(email='agent@test.com').exists():
                self.stdout.write(self.style.WARNING('Test agent already exists'))
                return
            
            # Create test agent
            agent = User.objects.create_user(
                username='testagent',
                email='agent@test.com',
                password='agent123',
                first_name='Test',
                last_name='Agent',
                role='agent',
                is_staff=False,
                is_superuser=False,
                is_active=True,
                status='active',
                profile_visible=True
            )
            
            self.stdout.write(self.style.SUCCESS('✅ Test agent created successfully'))
            self.stdout.write(f'✅ Email: agent@test.com')
            self.stdout.write(f'✅ Password: agent123')
            self.stdout.write(f'✅ Role: {agent.role}')
            self.stdout.write(f'✅ Status: {agent.status}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error creating test agent: {e}'))
