import json
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.contrib.auth import get_user_model
from portfolios.models import Category

User = get_user_model()


class Command(BaseCommand):
    help = 'Load photographer category fixtures and assign them to a user'

    def add_arguments(self, parser):
        parser.add_argument(
            'username',
            type=str,
            nargs='?',
            default=None,
            help='Username of the photographer to assign fixtures to'
        )

    def handle(self, *args, **options):
        username = options['username']
        
        # Prompt for username if not provided
        if not username:
            username = input('Enter the username to add categories: ').strip()
            if not username:
                raise CommandError('Username cannot be empty')

        # Check if user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist')

        # Load the fixture file
        fixture_path = 'portfolios/fixtures/categories/photographer.json'
        
        try:
            with open(fixture_path, 'r') as f:
                fixture_data = json.load(f)
        except FileNotFoundError:
            raise CommandError(f'Fixture file not found at {fixture_path}')
        except json.JSONDecodeError:
            raise CommandError(f'Invalid JSON in fixture file {fixture_path}')

        # Process fixture data and create categories for the user
        created_count = 0
        for item in fixture_data:
            if item.get('model') != 'portfolios.category':
                continue

            fields = item.get('fields', {})
            
            # Check if category already exists for this user
            category_name = fields.get('name')
            if Category.objects.filter(user=user, name=category_name).exists():
                self.stdout.write(
                    self.style.WARNING(
                        f'Category "{category_name}" already exists for user "{username}", skipping...'
                    )
                )
                continue

            # Create the category
            try:
                category = Category.objects.create(
                    user=user,
                    name=fields.get('name'),
                    name_ar=fields.get('name_ar'),
                    icon=fields.get('icon'),
                    description=fields.get('description'),
                    description_ar=fields.get('description_ar'),
                    features=fields.get('features', []),
                    order=fields.get('order', 0)
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created category: {category.name} / {category.name_ar}'
                    )
                )
                created_count += 1
            except Exception as e:
                raise CommandError(f'Error creating category "{category_name}": {str(e)}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {created_count} category(ies) for user "{username}"'
            )
        )
