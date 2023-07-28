"""
Django settings for simple_expenses project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from enum import Enum
from pathlib import Path
from typing import List

from pydantic import BaseModel
from pydantic.networks import IPv4Address
from pydantic_settings import BaseSettings, SettingsConfigDict


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class DatabaseEngineEnum(str, Enum):
    SQLITE = "sqlite"
    POSTGRES = "postgres"


class DatabaseConfig(BaseModel):
    engine: DatabaseEngineEnum = DatabaseEngineEnum.SQLITE
    name: str = BASE_DIR / "db.sqlite3"
    user: str = None
    password: str = None
    host: str = None
    port: int = None

    def to_dict(self):
        if self.engine == DatabaseEngineEnum.SQLITE:
            return {"ENGINE": "django.db.backends.sqlite3", "NAME": self.name}
        elif self.engine == DatabaseEngineEnum.POSTGRES:
            return {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": self.name,
                "USER": self.user,
                "PASSWORD": self.password,
                "HOST": self.host,
                "PORT": self.port,
            }
        else:
            raise ValueError(f"Invalid DatabaseEngineEnum={self.engine}")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="simple_exp_",
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    secret_key: str = "django-insecure-1)gcxgc9zc15-=%1438tib=w-wovi=gouk#rbpsydm##9xf3uc"
    debug: bool = True
    allowed_hosts: List[IPv4Address] = ["simple-expenses.podewitz.local"]
    db: DatabaseConfig = DatabaseConfig()

    language_code: str = "en-us"
    time_zone: str = "UTC"
    use_i18n: bool = True
    use_tz: bool = True

    static_url: str = "static/"
    static_root: str = "/app/static"


config = Settings()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.debug

ALLOWED_HOSTS = config.allowed_hosts


# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "transactions.apps.TransactionsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "simple_expenses.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "simple_expenses.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {"default": config.db.to_dict()}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = config.language_code

TIME_ZONE = config.time_zone

USE_I18N = config.use_i18n

USE_TZ = config.use_tz


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = config.static_url

STATIC_ROOT = config.static_root

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
