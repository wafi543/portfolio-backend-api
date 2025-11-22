from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Abstract User model that extends Django's built-in User.
    Add custom fields here that should be shared across user types.
    """
    job_title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Job title of the user"
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Phone number of the user"
    )
    location = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        help_text="Location of the user"
    )
    about_me = models.TextField(
        max_length=2000,
        blank=True,
        null=True,
        help_text="About me section in English"
    )
    about_me_ar = models.TextField(
        max_length=2000,
        blank=True,
        null=True,
        help_text="About me section in Arabic"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.get_full_name()} - {self.job_title or 'No job title'}"


class User(CustomUser):
    """
    Concrete User model for database storage.
    Inherits from the abstract CustomUser model.
    """
    class Meta:
        db_table = 'auth_user'
