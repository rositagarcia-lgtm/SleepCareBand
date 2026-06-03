from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================
# CONFIGURACIÓN GENERAL
# =========================================

SECRET_KEY = 'django-insecure-z)bc(=%5v$a7xhr191r^juu#e6@bdoz*n4h=bf3@&v2cp4uu)g'

DEBUG = True

ALLOWED_HOSTS = ["*"]


# =========================================
# APLICACIONES
# =========================================

INSTALLED_APPS = [

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "monitoreo",
    "rest_framework",

]


# =========================================
# MIDDLEWARE
# =========================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================
# URLS
# =========================================

ROOT_URLCONF = "sleepcare.urls"


# =========================================
# TEMPLATES
# =========================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =========================================
# WSGI
# =========================================

WSGI_APPLICATION = "sleepcare.wsgi.application"


# =========================================
# BASE DE DATOS SQLITE
# =========================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "sleepcare_db",
        "USER": "root",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}

# =========================================
# VALIDACIÓN DE PASSWORDS
# =========================================

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


# =========================================
# IDIOMA Y ZONA HORARIA
# =========================================

LANGUAGE_CODE = "es-pe"

TIME_ZONE = "America/Lima"

USE_I18N = True

USE_TZ = True


# =========================================
# ARCHIVOS ESTÁTICOS
# =========================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================
# CONFIGURACIÓN UNFOLD
# =========================================

UNFOLD = {

    # -------- Información General --------

    "SITE_TITLE": "SleepCare Admin",

    "SITE_HEADER": "SleepCare Band PRO+",

    "SITE_SUBHEADER": "Sistema Inteligente de Monitoreo de Sueño",

    "SITE_SYMBOL": "monitor_heart",


    # -------- Logo --------

    "SITE_ICON": {
        "light": "/static/img/logo.png",
        "dark": "/static/img/logo.png",
    },

    "SITE_LOGO": {
        "light": "/static/img/logo.png",
        "dark": "/static/img/logo.png",
    },


    # -------- CSS Personalizado --------

    


    "STYLES": [
        lambda request: "/static/css/admin.css",
    ],



    # -------- Opciones --------

    "SHOW_HISTORY": True,

    "SHOW_VIEW_ON_SITE": False,

    "SHOW_BACK_BUTTON": True,


    # -------- Colores --------

    "COLORS": {
        "primary": {

            "50": "239 246 255",
            "100": "219 234 254",
            "200": "191 219 254",
            "300": "147 197 253",
            "400": "96 165 250",
            "500": "59 130 246",
            "600": "37 99 235",
            "700": "29 78 216",
            "800": "30 64 175",
            "900": "30 58 138",
            "950": "23 37 84",

        },
    },


    # -------- Sidebar --------

    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
    },

}