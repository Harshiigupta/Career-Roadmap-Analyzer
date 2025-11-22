
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-assignment-key"  # for local use only

DEBUG = True
ALLOWED_HOSTS = ["*"]

# ----------------------------------------------------
# REQUIRED DJANGO APPS (Your biggest error)
# ----------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "careerapp",
]

MIDDLEWARE = [
     "django.middleware.security.SecurityMiddleware",

    # WhiteNoise for static files
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",

    
  #  "django.middleware.common.CommonMiddleware",
 #    "django.middleware.security.SecurityMiddleware",
  #  "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "career_project.urls"

TEMPLATES = [
    {
        # "BACKEND": "django.template.backends.django.DjangoTemplates",
        # "DIRS": [BASE_DIR / "careerapp" / "templates"],
        # "APP_DIRS": True,
        # "OPTIONS": {},
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "careerapp" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]
    


WSGI_APPLICATION = "career_project.wsgi.application"

# No DB required - use sqlite default if migrations used (not necessary)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "careerapp" / "static"]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
