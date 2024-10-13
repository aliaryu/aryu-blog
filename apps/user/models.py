from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from apps.core.models import (
    SoftDeleteModel,
    SoftDeleteManager,
)


class UserManager(SoftDeleteManager, BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        if not password:
            raise ValueError(_("The Password must be set"))

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class UserRelatedManager(SoftDeleteManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False, user__is_deleted=False)


class User(SoftDeleteModel, AbstractUser):
    username = None

    email = models.EmailField(
        verbose_name = _("email"),
        max_length = 255,
        unique = True,
    )

    is_active = models.BooleanField(
        verbose_name = _("active"),
        default = False,
        help_text = _(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"{self.email}"

