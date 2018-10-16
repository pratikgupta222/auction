from django.db import models

# Create your models here.
import logging
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils import timezone
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
# from django_otp.oath import totp
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Create and Save an User with email and password
            :param str email: user email
            :param str password: user password
            :param bool is_staff: whether user staff or not
            :param bool is_superuser: whether user admin or not
            :return users.models.User user: user
            :raise ValueError: email is not set
        """
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)

        user = self.model(email=email, is_staff=is_staff,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save an User with email and password
        :param str email: user email
        :param str password: user password
        :return users.models.User user: regular user
        """
        is_staff = extra_fields.pop("is_staff", False)
        return self._create_user(email, password, is_staff, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save an User with the given email and password.
        :param str email: user email
        :param str password: user password
        :return users.models.User user: admin user
        """
        return self._create_user(email, password, True, True,
                                 **extra_fields)

    def do_login(self, request, email=None,
                 password=None, user=None, **extra_fields):
        """
            Returns the JWT token in case of success, returns the error response in case of login failed.
        """
        if user:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
        else:
            if not email:
                return Response(status=status.HTTP_400_BAD_REQUEST, data='Email is mandatory.')

            user = authenticate(email=email, password=password)

        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data='Incorrect email or password')

        # Login the User
        login(request, user)
        token = self.generate_auth_token(user)

        response = {
            'token': token,
            'user': user
        }
        return Response(status=status.HTTP_200_OK, data=response)

    def _set_response(self, is_success, _status, message):
        return {
            'is_success': is_success,
            'status': _status,
            'message': message
        }

    # def do_login_new(self, request, email=None,
    #                  password=None, user=None, **extra_fields):
    #     """
    #         Returns the JWT token in case of success, returns the error response in case of login failed.
    #     """
    #     if user:
    #         user.backend = 'django.contrib.auth.backends.ModelBackend'
    #     else:
    #         if not email:
    #             return self._set_response(
    #                 False, status.HTTP_400_BAD_REQUEST,
    #                 LOGIN_VALIDATION_MESSAGES['email_required'])

    #         user = authenticate(email=email, password=password)

    #     if user is None:
    #         return self._set_response(
    #             False, status.HTTP_401_UNAUTHORIZED,
    #             LOGIN_VALIDATION_MESSAGES['invalid_credentials'])

    #     if not user.is_active:
    #         return self._set_response(
    #             False, status.HTTP_401_UNAUTHORIZED,
    #             LOGIN_VALIDATION_MESSAGES['activation_pending'])

    #     login(request, user)
    #     token = self.generate_auth_token(user)

    #     message = {
    #         'token': token,
    #         'user': user
    #     }
    #     return self._set_response(True, status.HTTP_200_OK, message)

    def generate_auth_token(self, user):
        # Generating the JWT Token
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(
        _('Name of User'), blank=True, max_length=255, db_index=True)

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True
    )

    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=_(
            'Designates whether the user can log into this admin site.'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email
