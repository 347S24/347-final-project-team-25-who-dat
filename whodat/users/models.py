from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models

class User(AbstractUser):
    """
    Default custom user model for Ultimate whodat.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    
    phone_number = models.CharField(max_length=15, blank=True)
    # roles = models.ManyToManyField(Role)
    photo = models.ImageField(upload_to='user_photos/', blank=True)
    preferred_name = models.CharField(max_length=100, blank=True)
    pronouns = models.CharField(max_length=50, blank=True)

    # Custom related_name for groups and user_permissions
    # groups = models.ManyToManyField(Group, related_name='homepage_users_groups')
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     verbose_name='user permissions',
    #     blank=True,
    #     related_name='homepage_users_permissions'
    # )

    def update_profile(self, **kwargs):
        for field, value in kwargs.items():
            if hasattr(self, field):
                setattr(self, field, value)
        self.save()

    def __str__(self):
        return self.username

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
