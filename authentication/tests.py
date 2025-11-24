from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.translation import activate
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

User = get_user_model()


class AuthenticationTranslationTestCase(APITestCase):
    """Test authentication endpoints with translation support"""

    def setUp(self):
        """Set up test client and user"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_login_invalid_credentials_english(self):
        """Test login with wrong credentials returns English error"""
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid credentials', str(response.data))

    def test_login_invalid_credentials_arabic(self):
        """Test login with wrong credentials returns Arabic error"""
        self.client.credentials(HTTP_ACCEPT_LANGUAGE='ar')
        
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('بيانات الدخول غير صحيحة', str(response.data))

    def test_login_success(self):
        """Test successful login returns tokens"""
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_logout_authenticated(self):
        """Test logout when authenticated"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post('/api/auth/logout/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_refresh_token_english(self):
        """Test invalid refresh token returns English error"""
        response = self.client.post('/api/auth/token/refresh/', {
            'refresh': 'invalid.token.here'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid refresh token', str(response.data))

    def test_invalid_refresh_token_arabic(self):
        """Test invalid refresh token returns Arabic error"""
        self.client.credentials(HTTP_ACCEPT_LANGUAGE='ar')
        
        response = self.client.post('/api/auth/token/refresh/', {
            'refresh': 'invalid.token.here'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('رمز التحديث', str(response.data))

    def test_me_endpoint_authenticated(self):
        """Test /me endpoint returns user data when authenticated"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/auth/me/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_me_endpoint_unauthenticated(self):
        """Test /me endpoint returns 401 when not authenticated"""
        response = self.client.get('/api/auth/me/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PasswordChangeTranslationTestCase(APITestCase):
    """Test password change endpoints with translation support"""

    def setUp(self):
        """Set up test client and user"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_password_change_wrong_old_password_english(self):
        """Test wrong old password error in English"""
        response = self.client.post('/api/auth/password-change/', {
            'old_password': 'wrongpassword',
            'new_password': 'newpass123'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Old password is not correct', str(response.data))

    def test_password_change_wrong_old_password_arabic(self):
        """Test wrong old password error in Arabic"""
        self.client.credentials(HTTP_ACCEPT_LANGUAGE='ar')
        
        response = self.client.post('/api/auth/password-change/', {
            'old_password': 'wrongpassword',
            'new_password': 'newpass123'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('كلمة المرور القديمة', str(response.data))

    def test_password_change_success_english(self):
        """Test successful password change returns English message"""
        response = self.client.post('/api/auth/password-change/', {
            'old_password': 'testpass123',
            'new_password': 'newpass123456'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Password changed successfully', str(response.data))

    def test_password_change_success_arabic(self):
        """Test successful password change returns Arabic message"""
        self.client.credentials(HTTP_ACCEPT_LANGUAGE='ar')
        
        response = self.client.post('/api/auth/password-change/', {
            'old_password': 'testpass123',
            'new_password': 'newpass123456'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('تم تغيير كلمة المرور', str(response.data))

    def test_password_change_new_password_too_similar_to_username(self):
        """Test that new password cannot be too similar to username"""
        response = self.client.post('/api/auth/password-change/', {
            'old_password': 'testpass123',
            'new_password': 'testuser'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_change_new_password_too_common(self):
        """Test that new password cannot be a common password"""
        response = self.client.post('/api/auth/password-change/', {
            'old_password': 'testpass123',
            'new_password': 'password'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LanguageActivationTestCase(TestCase):
    """Test language activation and translation loading"""

    def test_activate_arabic_language(self):
        """Test activating Arabic language"""
        from django.utils.translation import get_language
        
        activate('ar')
        self.assertEqual(get_language(), 'ar')

    def test_activate_english_language(self):
        """Test activating English language"""
        from django.utils.translation import get_language
        
        activate('en')
        self.assertEqual(get_language(), 'en')

    def test_translation_string_format_lazy(self):
        """Test format_lazy with translated strings"""
        from django.utils.text import format_lazy
        from django.utils.translation import gettext_lazy as _
        
        activate('ar')
        msg = format_lazy(_('Image size ({} MB) exceeds 5MB limit'), '5.50')
        msg_str = str(msg)
        
        self.assertIn('حجم الصورة', msg_str)
        self.assertIn('5.50 MB', msg_str)
