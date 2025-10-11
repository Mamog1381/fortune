from django.core.management.base import BaseCommand
from django.conf import settings
from fortune.services import OpenRouterService


class Command(BaseCommand):
    help = 'Check OpenRouter.ai API configuration and status'

    def handle(self, *args, **options):
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.HTTP_INFO('  OpenRouter.ai API Status Check'))
        self.stdout.write('='*60 + '\n')

        # Check if API key is configured
        api_key = settings.OPENROUTER_API_KEY

        if not api_key or api_key == '':
            self.stdout.write(self.style.WARNING('⚠ API Key Status: NOT CONFIGURED'))
            self.stdout.write('\n' + self.style.WARNING('Mode: MOCK/DEMO MODE'))
            self.stdout.write('\nThe system will work with mock responses for testing.')
            self.stdout.write('Features will return demonstration fortune readings.\n')

            self.stdout.write('\n' + '─'*60)
            self.stdout.write('\nTo enable real AI-powered readings:')
            self.stdout.write('\n  1. Visit: https://openrouter.ai/keys')
            self.stdout.write('  2. Create an account and generate an API key')
            self.stdout.write('  3. Add the key to your .env file:')
            self.stdout.write('     OPENROUTER_API_KEY=your-key-here')
            self.stdout.write('  4. Restart the application')
            self.stdout.write('\n' + '─'*60 + '\n')
        else:
            # Show masked key
            masked_key = api_key[:8] + '...' + api_key[-4:] if len(api_key) > 12 else '***'
            self.stdout.write(self.style.SUCCESS('✓ API Key Status: CONFIGURED'))
            self.stdout.write(f'  Key: {masked_key}\n')

            # Test API connection
            self.stdout.write('Testing API connection...')

            service = OpenRouterService()
            status = service.check_api_status()

            if status['working']:
                self.stdout.write(self.style.SUCCESS('✓ API Connection: WORKING'))
                self.stdout.write(self.style.SUCCESS('✓ Status: All systems operational\n'))
            else:
                self.stdout.write(self.style.ERROR('✗ API Connection: FAILED'))
                self.stdout.write(f'  Error: {status["message"]}\n')
                self.stdout.write('\nPlease check:')
                self.stdout.write('  - Your API key is valid')
                self.stdout.write('  - You have sufficient credits')
                self.stdout.write('  - Network connection is working\n')

        # Show available features
        from fortune.models import FortuneFeature

        active_features = FortuneFeature.objects.filter(is_active=True).count()
        total_features = FortuneFeature.objects.count()

        self.stdout.write('─'*60)
        self.stdout.write(f'\nFortune Features in Database:')
        self.stdout.write(f'  Active: {active_features}')
        self.stdout.write(f'  Total: {total_features}')

        if total_features == 0:
            self.stdout.write('\n' + self.style.WARNING('⚠ No features found!'))
            self.stdout.write('\nRun: python manage.py populate_features')
            self.stdout.write('to add the default fortune-telling features.\n')
        else:
            self.stdout.write('\n' + self.style.SUCCESS('✓ Features loaded\n'))

            # List features
            features = FortuneFeature.objects.filter(is_active=True)
            if features.exists():
                self.stdout.write('\nAvailable Features:')
                for feature in features:
                    icon = '🖼️' if 'image' in feature.input_type else '✍️'
                    self.stdout.write(f'  {icon} {feature.name} ({feature.feature_type})')

        self.stdout.write('\n' + '='*60 + '\n')
