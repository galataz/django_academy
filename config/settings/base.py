from pathlib import Path
import os
BASE_DIR=Path(__file__).resolve().parents[2]
SECRET_KEY=os.environ.get('SECRET_KEY','local-development-only-change-before-deploy')
DEBUG=False
ALLOWED_HOSTS=['localhost','127.0.0.1','testserver']
INSTALLED_APPS=['django.contrib.contenttypes','django.contrib.staticfiles','rest_framework','academy']
MIDDLEWARE=['django.middleware.security.SecurityMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF='config.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'templates'],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request','academy.context_processors.course_context']}}]
DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'db.sqlite3'}}
STATIC_URL='/static/'
STATICFILES_DIRS=[BASE_DIR/'static']
STATIC_ROOT=BASE_DIR/'staticfiles'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
TIME_ZONE='America/Bogota'
USE_TZ=True
LANGUAGE_CODE='es'
REST_FRAMEWORK={'DEFAULT_AUTHENTICATION_CLASSES':[],'DEFAULT_PERMISSION_CLASSES':['rest_framework.permissions.AllowAny'],'UNAUTHENTICATED_USER':None}

# Seguridad común. La academia pública no crea sesiones de usuario;
# estas opciones también documentan la política si una app usa sesiones.
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 1200  # ventana de 20 minutos para una sesión que se utilice
SESSION_SAVE_EVERY_REQUEST = True  # expiración deslizante, no límite absoluto

# Compatible con clientes AJAX que leen csrftoken. HttpOnly sobre esta
# cookie no sustituye el escape de HTML ni evita por sí mismo XSS.
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_NAME = 'csrftoken'

# XFrameOptionsMiddleware protege las páginas. El laboratorio tiene una
# excepción SAMEORIGIN localizada para permitir su iframe en el curso.
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'same-origin'
