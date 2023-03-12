from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUserManger(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email"))

    def create_user(
        self, username, email, password, first_name, **extra_fields
    ):
        if not username:
            raise ValidationError(_("User must submit username"))
        if not first_name:
            raise ValidationError(_("User must submit first_name"))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Base User Account : email field is required"))

        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
           **extra_fields
        )

        user.set_password(password)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, email, password, first_name, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("superusers must have be staff"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("superusers must have be suoeruser"))

        if not password:
            raise ValueError(_("superusers must have password"))
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("email must be provided"))

        user = self.create_user(
            username, email, password, first_name, **extra_fields
        )
        user.save(using=self._db)
        return user