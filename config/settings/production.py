"""Configuración HTTPS de producción; valores privados desde el entorno."""
from .base import *
from django.core.exceptions import ImproperlyConfigured


DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = [host.strip() for host in os.environ['ALLOWED_HOSTS'].split(',') if host.strip()]
if not ALLOWED_HOSTS or any(host == '*' or '://' in host or '/' in host for host in ALLOWED_HOSTS):
    raise ImproperlyConfigured('ALLOWED_HOSTS requiere hosts explícitos sin esquema ni rutas')
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if origin.strip()]

# Transporte: el sitio productivo se sirve bajo HTTPS.
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# El proxy de producción debe eliminar/sobrescribir el header del cliente
# y no permitir acceso directo que eluda esa frontera de confianza.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Política HSTS del proyecto de referencia: un año y todo el alcance.
# Requiere HTTPS correcto en todos los subdominios incluidos.
# PRELOAD anuncia la directiva; no realiza la inscripción externa.
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}
MIDDLEWARE = [MIDDLEWARE[0], 'whitenoise.middleware.WhiteNoiseMiddleware', *MIDDLEWARE[1:]]
