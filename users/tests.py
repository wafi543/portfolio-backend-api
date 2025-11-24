from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

User = get_user_model()


class UserModelTestCase(TestCase):
    """Test user model functionality"""

    def test_create_user(self):
        """Test creating a user"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_user_custom_fields(self):
        """Test user custom fields"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        user.job_title = 'Designer'
        user.phone_number = '1234567890'
        user.location = 'New York'
        user.about_me = 'I am a designer'
        user.about_me_ar = 'أنا مصمم'
        user.bio = 'Professional designer'
        user.bio_ar = 'مصمم محترف'
        user.save()
        
        user.refresh_from_db()
        
        self.assertEqual(user.job_title, 'Designer')
        self.assertEqual(user.phone_number, '1234567890')
        self.assertEqual(user.location, 'New York')
        self.assertEqual(user.about_me, 'I am a designer')
        self.assertEqual(user.about_me_ar, 'أنا مصمم')
        self.assertEqual(user.bio, 'Professional designer')
        self.assertEqual(user.bio_ar, 'مصمم محترف')

    def test_user_get_full_name(self):
        """Test user full name"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        
        self.assertEqual(user.get_full_name(), 'John Doe')

    def test_superuser_creation(self):
        """Test creating a superuser"""
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)


class UserSerializerTestCase(APITestCase):
    """Test user serializer"""

    def test_user_serializer_representation(self):
        """Test that user serializer returns correct fields"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        
        from users.serializers import UserSerializer
        serializer = UserSerializer(user)
        
        self.assertEqual(serializer.data['username'], 'testuser')
        self.assertEqual(serializer.data['email'], 'test@example.com')
        self.assertEqual(serializer.data['first_name'], 'John')
        self.assertEqual(serializer.data['last_name'], 'Doe')
        self.assertIn('id', serializer.data)
