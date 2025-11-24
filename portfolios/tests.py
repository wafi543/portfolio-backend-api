from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils.translation import activate, get_language
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
import io
from PIL import Image

from .models import Category, Portfolio

User = get_user_model()


class TranslationTestCase(TestCase):
    """Test cases for Arabic translation functionality"""

    def setUp(self):
        """Set up test user and categories"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            user=self.user,
            name='Design',
            name_ar='تصميم'
        )

    def test_invalid_credentials_translation(self):
        """Test that 'Invalid credentials' is translated to Arabic"""
        activate('ar')
        from django.utils.translation import gettext as _trans
        
        msg = _trans('Invalid credentials')
        self.assertEqual(msg, 'بيانات الدخول غير صحيحة')

    def test_password_change_success_translation(self):
        """Test password change success message is translated"""
        activate('ar')
        from django.utils.translation import gettext as _trans
        
        msg = _trans('Password changed successfully')
        self.assertEqual(msg, 'تم تغيير كلمة المرور بنجاح')

    def test_old_password_incorrect_translation(self):
        """Test old password error is translated"""
        activate('ar')
        from django.utils.translation import gettext as _trans
        
        msg = _trans('Old password is not correct')
        self.assertEqual(msg, 'كلمة المرور القديمة غير صحيحة')

    def test_invalid_refresh_token_translation(self):
        """Test invalid refresh token is translated"""
        activate('ar')
        from django.utils.translation import gettext as _trans
        
        msg = _trans('Invalid refresh token')
        self.assertEqual(msg, 'رمز التحديث غير صالح')

    def test_category_name_validation_translation(self):
        """Test category name validation error is translated"""
        activate('ar')
        from django.utils.translation import gettext as _trans
        
        msg = _trans('Category name must contain only English alphabetical characters and spaces.')
        self.assertEqual(msg, 'يجب أن يحتوي اسم الفئة على أحرف إنجليزية وفراغات فقط.')

    def test_category_arabic_name_validation_translation(self):
        """Test category Arabic name validation error is translated"""
        activate('ar')
        from django.utils.translation import gettext as _trans
        
        msg = _trans('Category Arabic name must contain only Arabic characters and spaces.')
        self.assertEqual(msg, 'يجب أن يحتوي الاسم العربي للفئة على أحرف عربية وفراغات فقط.')

    def test_image_size_exceeded_translation_with_format(self):
        """Test image size exceeded message with dynamic size is translated"""
        activate('ar')
        from django.utils.translation import gettext_lazy as _lazy
        
        msg = format_lazy(_lazy('Image size ({} MB) exceeds 5MB limit'), '5.50')
        self.assertIn('حجم الصورة', str(msg))
        self.assertIn('5.50 MB', str(msg))
        self.assertIn('يتجاوز حد 5MB', str(msg))

    def test_category_selection_requires_auth_translation(self):
        """Test category selection auth error is translated"""
        activate('ar')
        from django.utils.translation import gettext as _trans
        
        msg = _trans('Category selection requires authentication.')
        self.assertEqual(msg, 'اختيار الفئة يتطلب المصادقة.')

    def test_category_not_found_translation(self):
        """Test category not found error is translated"""
        activate('ar')
        from django.utils.translation import gettext as _trans
        
        msg = _trans('Category does not exist or does not belong to you.')
        self.assertEqual(msg, 'الفئة غير موجودة أو لا تنتمي إليك.')

    def test_category_deletion_protection_translation(self):
        """Test category deletion protection message is translated"""
        activate('ar')
        from django.utils.translation import gettext as _trans
        
        msg = _trans('Cannot delete category with associated portfolios. Please reassign or delete the portfolios first.')
        self.assertEqual(msg, 'لا يمكن حذف التصنيف الذي يحتوي على أعمال مرتبطة. يرجى إعادة تعيين أو حذف الأعمال أولاً.')

    def test_portfolio_info_not_found_translation(self):
        """Test portfolio info not found error is translated"""
        activate('ar')
        from django.utils.translation import gettext as _trans
        
        msg = _trans('Portfolio info not found')
        self.assertEqual(msg, 'لم يتم العثور على معلومات العمل')

    def test_language_resets_after_activation(self):
        """Test that language is properly reset after deactivation"""
        activate('ar')
        self.assertEqual(get_language(), 'ar')
        
        activate('en')
        self.assertEqual(get_language(), 'en')


class CategoryValidationTranslationTestCase(APITestCase):
    """Test category validation with translation"""

    def setUp(self):
        """Set up test client and user"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_category_invalid_english_name_error_translated(self):
        """Test that category name validation error returns translated message"""
        self.client.credentials(HTTP_ACCEPT_LANGUAGE='ar')
        
        response = self.client.post('/api/portfolio/categories/', {
            'name': 'Design123',  # Contains numbers - invalid
            'name_ar': 'تصميم'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('اسم الفئة', str(response.data))

    def test_category_invalid_arabic_name_error_translated(self):
        """Test that Arabic category name validation error is translated"""
        self.client.credentials(HTTP_ACCEPT_LANGUAGE='ar')
        
        response = self.client.post('/api/portfolio/categories/', {
            'name': 'Design',
            'name_ar': 'تصميم123'  # Contains numbers - invalid
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('عربية', str(response.data))


class PortfolioImageValidationTestCase(APITestCase):
    """Test portfolio image size validation with translation"""

    def setUp(self):
        """Set up test client, user, and category"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.category = Category.objects.create(
            user=self.user,
            name='Photography',
            name_ar='التصوير'
        )

    def create_large_image(self, size_mb=6):
        """Create a test image larger than 5MB"""
        # Create image with size > 5MB
        size_pixels = int((size_mb * 1024 * 1024) ** 0.5)  # Rough approximation
        image = Image.new('RGB', (size_pixels, size_pixels), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG', quality=95)
        image_io.seek(0)
        return image_io

    def test_image_size_exceeded_error_translated(self):
        """Test that oversized image error is translated"""
        self.client.credentials(HTTP_ACCEPT_LANGUAGE='ar')
        
        large_image = self.create_large_image(size_mb=6)
        
        response = self.client.post('/api/portfolio/', {
            'title': 'Test Portfolio',
            'subtitle': 'Test subtitle',
            'body': 'Test body',
            'category_id': self.category.id,
            'image': large_image
        }, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that the response contains Arabic text for image size error
        self.assertIn('حجم الصورة', str(response.data) or 'image' in str(response.data).lower())


class AuthenticationTranslationTestCase(APITestCase):
    """Test authentication-related translations"""

    def setUp(self):
        """Set up test client and user"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_invalid_credentials_error_with_accept_language_header(self):
        """Test login with wrong credentials returns Arabic error"""
        self.client.credentials(HTTP_ACCEPT_LANGUAGE='ar')
        
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('بيانات الدخول غير صحيحة', str(response.data))

    def test_invalid_refresh_token_error_with_accept_language_header(self):
        """Test invalid refresh token returns Arabic error"""
        self.client.credentials(HTTP_ACCEPT_LANGUAGE='ar')
        
        response = self.client.post('/api/auth/token/refresh/', {
            'refresh': 'invalid.token.here'
        })
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('رمز التحديث', str(response.data))


class PasswordChangeTranslationTestCase(APITestCase):
    """Test password change with translations"""

    def setUp(self):
        """Set up test client and user"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_old_password_incorrect_with_accept_language_header(self):
        """Test old password error is returned in Arabic"""
        self.client.credentials(HTTP_ACCEPT_LANGUAGE='ar')
        
        response = self.client.post('/api/auth/password-change/', {
            'old_password': 'wrongpassword',
            'new_password': 'newpass123'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('كلمة المرور القديمة', str(response.data))

    def test_password_change_success_with_accept_language_header(self):
        """Test password change success message is in Arabic"""
        self.client.credentials(HTTP_ACCEPT_LANGUAGE='ar')
        
        response = self.client.post('/api/auth/password-change/', {
            'old_password': 'testpass123',
            'new_password': 'newpass123'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('تم تغيير كلمة المرور', str(response.data))
