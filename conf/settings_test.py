# settings_test.py
from .settings import *

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',  # faster for tests
]

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Use in-memory DB for speed (if supported)
DATABASES["default"]["NAME"] = ":memory:"