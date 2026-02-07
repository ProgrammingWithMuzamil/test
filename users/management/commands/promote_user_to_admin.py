from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Promote a user to admin role by email'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            required=True,
            help='Email address of the user to promote to admin'
        )

    def handle(self, *args, **options):
        email = options['email']
        
        try:
            user = User.objects.get(email=email)
            user.role = 'admin'
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully promoted {email} to admin role'
                )
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f'User with email {email} does not exist'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error promoting user: {str(e)}'
                )
            )
