from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from apps.core.models import (
    SoftDeleteModel,
    SoftDeleteManager,
    TimeStampModel,
)
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


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


class Profile(SoftDeleteModel, TimeStampModel):
    user = models.OneToOneField(
        verbose_name = _("user"),
        to = "User",
        on_delete = models.DO_NOTHING,
        related_name = "profile",
    )

    biography = models.TextField(
        verbose_name = _("biography"),
        blank = True,
        null = True,
    )

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    gender = models.CharField(
        verbose_name = _("gender"),
        max_length = 1, 
        choices = GENDER_CHOICES,
        blank = True,
        null = True,
    )

    birth_date = models.DateField(
        verbose_name = _("birth date"),
        blank = True,
        null = True,
    )

    phone_number = models.CharField(
        verbose_name = _("phone number"),
        max_length = 15,
        blank = True,
        null = True,
    )

    image = models.ImageField(
        verbose_name = _("image"),
        upload_to = "profile_image/",
        blank = True,
        null = True,
        validators = [
            FileExtensionValidator(
                allowed_extensions = ("jpg", "png")
            )
        ]
    )

    profile_view = models.PositiveIntegerField(
        verbose_name = _("profile view"),
        default = 1,
    )

    objects = UserRelatedManager()

    def clean(self):
        super().clean()
        if self.birth_date and self.birth_date > timezone.now().date():
            raise ValidationError({'birth_date': _("birth date cannot be in future.")})

        width, height = self.image.width, self.image.height
        if width != height:
            raise ValidationError({'image': _("image must be square.")})

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        return f"{self.user.email}"


class Follow(SoftDeleteModel, TimeStampModel):
    follower = models.ForeignKey(
        verbose_name = _("follower"),
        # supose user_id field, who start follow
        help_text = _("the one who follows"),
        to = "User",
        on_delete = models.DO_NOTHING,
        related_name = "followings",
    )

    following = models.ForeignKey(
        verbose_name = _("following"),
        # supose follow_for field, who who receives follow
        help_text = _("the one who is followed"),
        to = "User",
        on_delete = models.DO_NOTHING,
        related_name = "followers",
    )

    objects = SoftDeleteManager()

    def clean(self):
        super().clean()
        if self.follower == self.following:
            raise ValidationError({'follower': _("cant follow yourself.")})
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["follower", "following"],
                name = "unique_follow",
            ),

            models.CheckConstraint(
                condition = ~ models.Q(follower=models.F("following")),
                name="same_follower_following",
            ),
        ]

    def __str__(self):
        return f"'{self.follower.email}' follows '{self.following.email}'"
