from django.test import TestCase
from rest_framework.test import APIClient
from academy.models import Lesson
from academy.catalog import LESSONS
class PublicAcademyTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Lesson.objects.bulk_create([Lesson(number=x['id'],title=x['title'],concept=x['concept'],source_path=x['path']) for x in LESSONS])
    def test_every_lesson_is_public(self):
        self.assertEqual(self.client.get('/').status_code,200)
        for x in LESSONS:self.assertEqual(self.client.get(f"/tema/{x['id']}/").status_code,200)
        self.assertEqual(self.client.get('/tema/999/').status_code,404)
    def test_no_auth_routes(self):
        for url in ['/login/','/logout/','/admin/']:self.assertEqual(self.client.get(url).status_code,404)
    def test_catalog_pagination(self):
        r=self.client.get('/api/catalogo/?per_page=5').json()
        self.assertEqual(len(r['results']),5);self.assertEqual(r['total_count'],len(LESSONS))
    def test_invalid_pagination(self):
        for query in ['page=0','per_page=101','page=no','ordering=unknown']:
            self.assertEqual(self.client.get('/api/catalogo/?'+query).status_code,400)
    def test_public_calculation(self):
        api=APIClient(enforce_csrf_checks=True)
        response=api.post('/api/laboratorio/temperatura/',{'celsius':0},format='json')
        self.assertEqual(response.status_code,200);self.assertEqual(response.json()['fahrenheit'],32)
        self.assertEqual(api.post('/api/laboratorio/temperatura/',{'celsius':-274},format='json').status_code,400)
    def test_search(self):
        self.assertContains(self.client.get('/?q=MSAL'),'Identidad externa y MSAL')
        self.assertEqual(self.client.get('/api/catalogo/?search=MSAL').json()['total_count'], sum('msal' in (x['title'] + ' ' + x['concept']).casefold() for x in LESSONS))
    def test_health(self):
        self.assertEqual(self.client.get('/ready/').status_code,200)
        self.assertEqual(self.client.get('/health/').json()['status'],'ok')

    def test_units_and_teaching_structure(self):
        response = self.client.get('/?unit=1')
        self.assertContains(response, 'Diseñar antes de programar')
        self.assertNotContains(response, 'Proyecto final: conectar todas las piezas')
        lesson = self.client.get('/tema/17/')
        self.assertContains(lesson, 'Ver solución orientativa')
        self.assertContains(lesson, 'role-selector')
        self.assertNotContains(lesson, 'Fuente de la implementación')
    def test_catalog_loading_has_explicit_utf8(self):
        import runpy
        from pathlib import Path
        from unittest.mock import patch
        original = Path.read_text
        encodings = []
        def windows_read(path, *args, **kwargs):
            encodings.append(kwargs.get('encoding'))
            kwargs.setdefault('encoding', 'cp1252')
            return original(path, *args, **kwargs)
        with patch.object(Path, 'read_text', windows_read):
            runpy.run_path(str(Path(__file__).parent / 'catalog.py'))
        self.assertTrue(all(encoding == 'utf-8' for encoding in encodings))

    def test_azure_extension_navigation_and_references(self):
        from academy.catalog import UNITS
        self.assertContains(self.client.get('/biblioteca/'), f'{len(UNITS)} unidades')
        response = self.client.get('/?unit=9')
        self.assertContains(response, 'Correo SMTP nativo después del commit')
        self.assertNotContains(response, 'Diseñar antes de programar')
        for lesson in (item for item in LESSONS if item['id'] >= 34):
            page = self.client.get(f"/tema/{lesson['id']}/")
            self.assertContains(page, 'Para profundizar')
            self.assertContains(page, lesson['references'][0]['url'])
            for field in ('why', 'theory', 'steps', 'code', 'explain', 'pitfall', 'exercise', 'solution', 'checks'):
                self.assertTrue(lesson[field], (lesson['id'], field))
        self.assertContains(self.client.get('/tema/31/'), '/tema/50/')
        self.assertNotContains(self.client.get(f"/tema/{LESSONS[-1]['id']}/"), 'Siguiente tema')

    def test_database_and_maintenance_units(self):
        database_page = self.client.get('/?unit=10')
        self.assertContains(database_page, 'Migraciones y permisos para tablas futuras')
        self.assertNotContains(database_page, 'Kudu y diagnóstico de cuota')
        maintenance_page = self.client.get('/?unit=11')
        self.assertContains(maintenance_page, 'Reducir el plan: diagnóstico Bx a F1')
        self.assertNotContains(maintenance_page, 'Roles de runtime, migración y consulta')
        self.assertContains(self.client.get('/tema/40/'), '/ruta/planear/')
        self.assertContains(self.client.get('/tema/57/'), 'verify-full')
        self.assertContains(self.client.get('/tema/60/'), 'Tu turno')
        self.assertContains(self.client.get('/tema/61/'), 'Comparación orientativa de niveles')

    def test_visual_assets_and_accessible_maps(self):
        from pathlib import Path
        from django.conf import settings
        import xml.etree.ElementTree as ET
        from academy.catalog import UNITS
        root = Path(settings.BASE_DIR)
        for lesson in LESSONS:
            visual = lesson['visual']
            self.assertEqual(len(visual['nodes']), 4)
            for field in ('illustration', 'diagram'):
                asset = root / 'static' / visual[field]
                self.assertTrue(asset.is_file())
                if field == 'diagram':
                    ET.parse(asset)
                else:
                    self.assertEqual(asset.read_bytes()[:4], b'RIFF')
            page = self.client.get(f"/tema/{lesson['id']}/")
            self.assertContains(page, 'class="visual-node"', count=4)
            self.assertContains(page, 'class="map-step"', count=4)
            self.assertContains(page, 'Leer la explicación del mapa')
            self.assertContains(page, visual['diagram'])
        home = self.client.get('/biblioteca/')
        self.assertContains(home, 'visuals/course-map.svg')
        for unit in UNITS:
            self.assertContains(home, unit['illustration'])
            self.assertTrue((root / 'static' / unit['illustration']).is_file())

    def test_game_is_public_and_integrated(self):
        response = self.client.get('/laboratorio/')
        self.assertContains(response, 'ISLA DJANGO')
        self.assertContains(response, '/static/game.bundle.js')
        self.assertContains(response, 'id="fallback"')
        self.assertNotContains(self.client.get('/'), 'src="/laboratorio/"')
        self.assertNotContains(self.client.get('/tema/8/'), 'src="/laboratorio/"')
        self.assertNotContains(self.client.get('/tema/9/'), 'src="/laboratorio/"')

    def test_game_allows_same_origin_embedding_only(self):
        self.assertEqual(self.client.get('/laboratorio/').headers['X-Frame-Options'], 'SAMEORIGIN')
        self.assertEqual(self.client.get('/').headers['X-Frame-Options'], 'DENY')
        self.assertEqual(self.client.get('/tema/8/').headers['X-Frame-Options'], 'DENY')

    def test_learning_order_preserves_stable_identifiers(self):
        self.assertEqual(len(LESSONS), 78)
        self.assertEqual(len({x['id'] for x in LESSONS}), 78)
        from academy.catalog import JOURNEY
        for stage in JOURNEY:
            for index, pk in enumerate(stage['lessons']):
                response = self.client.get(f'/tema/{pk}/')
                expected_next = stage['lessons'][index + 1] if index + 1 < len(stage['lessons']) else None
                expected_previous = stage['lessons'][index - 1] if index else None
                self.assertEqual(response.context['next'], expected_next)
                self.assertEqual(response.context['previous'], expected_previous)
                self.assertEqual(response.context['stage']['slug'], stage['slug'])
            for pk in stage['electives']:
                page = self.client.get(f'/tema/{pk}/')
                self.assertTrue(page.context['is_extension'])
                self.assertIsNone(page.context['next'])
                self.assertContains(page, f'/ruta/{stage["slug"]}/#entrega')
        self.assertEqual(self.client.get('/tema/2/').context['next'], 62)
        self.assertEqual(self.client.get('/tema/3/').context['next'], 63)

    def test_deployment_curriculum_and_configurator(self):
        page = self.client.get('/?unit=8')
        for title in ('Variables de producción', 'Gunicorn o Daphne', 'Herramientas avanzadas', 'PowerShell', 'deploy.zip'):
            self.assertContains(page, title)
        self.assertContains(page, 'Etapas del despliegue')
        for pk in (41, 63, 65, 66):
            self.assertContains(self.client.get(f'/tema/{pk}/'), 'id="deploy-env"')
        lesson = self.client.get('/tema/41/')
        self.assertContains(lesson, 'http://localhost:8000/aad/callback')
        self.assertContains(lesson, 'App Service Authentication')
        self.assertContains(self.client.get('/tema/70/'), '--src-url')
        self.assertContains(self.client.get('/tema/67/'), 'STORAGES')

    def test_security_policy_matches_reference_values(self):
        import importlib
        import os
        from unittest.mock import patch
        from config.settings import base
        common = {
            'SESSION_COOKIE_HTTPONLY': True, 'CSRF_COOKIE_HTTPONLY': False,
            'SESSION_COOKIE_SAMESITE': 'Lax', 'CSRF_COOKIE_SAMESITE': 'Lax',
            'CSRF_COOKIE_NAME': 'csrftoken', 'X_FRAME_OPTIONS': 'DENY',
            'SESSION_COOKIE_AGE': 1200, 'SESSION_SAVE_EVERY_REQUEST': True,
            'SECURE_CONTENT_TYPE_NOSNIFF': True, 'SECURE_REFERRER_POLICY': 'same-origin',
        }
        for key, value in common.items():
            self.assertEqual(getattr(base, key), value, key)
        with patch.dict(os.environ, {'SECRET_KEY': 'test-key-only-' * 5, 'ALLOWED_HOSTS': 'academy.example'}):
            prod = importlib.import_module('config.settings.production')
        expected = {
            'DEBUG': False, 'SECURE_SSL_REDIRECT': True,
            'SECURE_PROXY_SSL_HEADER': ('HTTP_X_FORWARDED_PROTO', 'https'),
            'SECURE_HSTS_SECONDS': 31536000, 'SECURE_HSTS_INCLUDE_SUBDOMAINS': True,
            'SECURE_HSTS_PRELOAD': True, 'SESSION_COOKIE_SECURE': True,
            'CSRF_COOKIE_SECURE': True,
        }
        for key, value in expected.items():
            self.assertEqual(getattr(prod, key), value, key)
        for pk in (74, 75):
            response = self.client.get(f'/tema/{pk}/')
            self.assertContains(response, 'Qué hace cada ajuste')
            self.assertContains(response, 'Cómo verificarlo.')

    def test_production_transport_headers_cookies_and_csrf(self):
        import importlib
        import os
        import types
        from unittest.mock import patch
        from django.test import Client, override_settings
        from django.http import HttpResponse
        from django.urls import path
        from django.views.decorators.csrf import ensure_csrf_cookie
        with patch.dict(os.environ, {'SECRET_KEY': 'test-key-only-' * 5, 'ALLOWED_HOSTS': 'academy.example'}):
            prod = importlib.import_module('config.settings.production')
        @ensure_csrf_cookie
        def probe(request):
            request.session['example'] = True
            return HttpResponse('ok')
        routes = types.ModuleType('security_probe_urls')
        routes.urlpatterns = [path('probe/', probe)]
        config = {key: getattr(prod, key) for key in (
            'SECURE_SSL_REDIRECT', 'SECURE_PROXY_SSL_HEADER', 'SECURE_HSTS_SECONDS',
            'SECURE_HSTS_INCLUDE_SUBDOMAINS', 'SECURE_HSTS_PRELOAD',
            'SESSION_COOKIE_SECURE', 'CSRF_COOKIE_SECURE',
        )}
        config.update(ROOT_URLCONF=routes, ALLOWED_HOSTS=['academy.example'],
            CSRF_TRUSTED_ORIGINS=[],
            SESSION_ENGINE='django.contrib.sessions.backends.signed_cookies',
            MIDDLEWARE=[*prod.MIDDLEWARE[:2],
                'django.contrib.sessions.middleware.SessionMiddleware', *prod.MIDDLEWARE[2:]])
        with override_settings(**config):
            client = Client(enforce_csrf_checks=True)
            response = client.get('/probe/', HTTP_HOST='academy.example')
            self.assertEqual(response.status_code, 301)
            self.assertEqual(response['Location'], 'https://academy.example/probe/')
            response = client.get('/probe/', HTTP_HOST='academy.example', HTTP_X_FORWARDED_PROTO='https')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Strict-Transport-Security'], 'max-age=31536000; includeSubDomains; preload')
            self.assertEqual(response['X-Content-Type-Options'], 'nosniff')
            self.assertEqual(response['Referrer-Policy'], 'same-origin')
            self.assertEqual(response['X-Frame-Options'], 'DENY')
            self.assertTrue(response.cookies['sessionid']['secure'])
            self.assertTrue(response.cookies['sessionid']['httponly'])
            self.assertEqual(response.cookies['sessionid']['samesite'], 'Lax')
            self.assertEqual(response.cookies['sessionid']['max-age'], 1200)
            self.assertTrue(response.cookies['csrftoken']['secure'])
            self.assertFalse(response.cookies['csrftoken']['httponly'])
            self.assertEqual(client.post('/probe/', HTTP_HOST='academy.example', secure=True).status_code, 403)
            token = response.cookies['csrftoken'].value
            self.assertEqual(client.post('/probe/', HTTP_HOST='academy.example', secure=True, HTTP_X_CSRFTOKEN=token, HTTP_REFERER='https://academy.example/probe/').status_code, 200)
            self.assertEqual(client.post('/probe/', HTTP_HOST='academy.example', secure=True, HTTP_X_CSRFTOKEN=token, HTTP_ORIGIN='https://evil.example').status_code, 403)
            self.assertEqual(client.get('/probe/', HTTP_HOST='evil.example').status_code, 400)

    def test_story_has_one_complete_connected_route(self):
        from academy.catalog import STORY
        ids = [pk for chapter in STORY for pk in chapter['lessons']]
        self.assertEqual(ids, [item['id'] for item in LESSONS])
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(ids[-1], 33)
        for position, lesson in enumerate(LESSONS):
            page = self.client.get(f"/tema/{lesson['id']}/")
            self.assertContains(page, lesson['narrative']['title'])
            for paragraph in lesson['narrative']['paragraphs']:
                self.assertContains(page, paragraph)
            if position + 1 < len(LESSONS):
                following = LESSONS[position + 1]
                self.assertEqual(lesson['story']['next']['id'], following['id'])
                # El relato conserva la cronología; la navegación técnica sigue la ruta práctica.
            else:
                self.assertIsNone(page.context['next'])

    def test_two_consumers_share_pagination_and_scoped_counts(self):
        from rest_framework.test import APIRequestFactory
        from academy.views.queries.catalog import CatalogQuery
        class ShortCatalogQuery(CatalogQuery):
            def get_queryset(self):
                return super().get_queryset().filter(number__lte=10)
        factory = APIRequestFactory()
        for view, expected_total in ((CatalogQuery, len(LESSONS)), (ShortCatalogQuery, 10)):
            self.assertNotIn('get', view.__dict__)
            response = view.as_view()(factory.get('/', {'per_page': 3}))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['total_count'], expected_total)
            self.assertEqual(len(response.data['results']), 3)
            for params in ({'per_page': 0}, {'per_page': 101}, {'page': 'no'}, {'ordering': 'secret'}):
                self.assertEqual(view.as_view()(factory.get('/', params)).status_code, 400)
            empty = view.as_view()(factory.get('/', {'search': 'zz-no-matches-zz'}))
            self.assertEqual(empty.data['total_count'], 0)
            self.assertEqual(empty.data['results'], [])

    def test_continuous_story_covers_every_lesson_in_reading_order(self):
        from academy.catalog import NARRATIVE
        response = self.client.get('/historia/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(NARRATIVE['scenes']), {str(item['id']) for item in LESSONS})
        html = response.content.decode('utf-8')
        offsets = []
        for lesson in LESSONS:
            marker = f'id="escena-{lesson["id"]}"'
            self.assertContains(response, marker, count=1)
            offsets.append(html.index(marker))
            self.assertContains(response, f'/tema/{lesson["id"]}/#mapa')
        self.assertEqual(offsets, sorted(offsets))
        self.assertContains(self.client.get('/'), 'Leer la historia completa')
        self.assertEqual(response.headers['X-Frame-Options'], 'DENY')


    def test_industrial_acceptance_is_integrated_and_anonymous(self):
        from academy.catalog import get_lesson
        from pathlib import Path
        from django.conf import settings
        import json
        lesson = get_lesson(78)
        response = self.client.get('/tema/78/')
        self.assertIsNone(response.context['previous'])
        self.assertEqual(response.context['next'], 1)
        for expected in ('WAF', 'logout', 'RTO', 'RPO', 'SAST', 'No aplica', 'acta de compromiso'):
            self.assertContains(response, expected)
        self.assertContains(self.client.get('/?q=aceptación'), lesson['title'])
        self.assertContains(self.client.get('/historia/'), 'id="escena-78"', count=1)
        self.assertContains(response, 'guides/expediente-aceptacion-industrial.md')
        guide = (Path(settings.BASE_DIR) / 'static/guides/expediente-aceptacion-industrial.md').read_text(encoding='utf-8')
        content = (json.dumps(lesson, ensure_ascii=False) + json.dumps(lesson['narrative'], ensure_ascii=False) + guide).casefold()
        for forbidden in ('colgas', 'cinsa', 'cotranscol', 'vanti', 'cdtdegas', 'cdt de gas', 'aviancataca', '225010930', 'gmp250', 'sg-ti-003', 'csirt@'):
            self.assertNotIn(forbidden, content)
        self.assertEqual(len(lesson['table']['rows']), 29)
        self.assertEqual(len(lesson['sections']), 22)

    def test_journey_covers_all_lessons_and_starts_with_acceptance(self):
        from academy.catalog import JOURNEY, JOURNEY_ORDER
        all_ids = [pk for stage in JOURNEY for pk in stage['lessons'] + stage['electives']]
        self.assertEqual(len(JOURNEY), 7)
        self.assertEqual(len(all_ids), len(set(all_ids)))
        self.assertEqual(set(all_ids), {lesson['id'] for lesson in LESSONS})
        self.assertEqual(JOURNEY_ORDER[0], 78)
        self.assertEqual(JOURNEY_ORDER[-1], 33)
        home = self.client.get('/')
        self.assertContains(home, 'class="journey-card"', count=7)
        self.assertNotContains(home, 'class="card"')
        for stage in JOURNEY:
            page = self.client.get(f'/ruta/{stage["slug"]}/')
            self.assertEqual(page.status_code, 200)
            self.assertContains(page, stage['outcome'])
            for pk in stage['lessons'] + stage['electives']:
                self.assertContains(page, f'/tema/{pk}/')
        self.assertEqual(self.client.get('/ruta/no-existe/').status_code, 404)
        self.assertContains(self.client.get('/biblioteca/'), 'class="card"', count=78)
        self.assertEqual(home.context['course_order'], JOURNEY_ORDER)

    def test_acceptance_workshop_links_controls_to_implementation(self):
        from academy.catalog import ACCEPTANCE
        import json
        page = self.client.get('/ruta/vender/')
        self.assertContains(page, 'class="evidence-form"', count=12)
        for control in ACCEPTANCE:
            self.assertContains(page, f'id="control-{control["id"]}"')
            for pk in control['lessons']:
                self.assertIn(pk, {lesson['id'] for lesson in LESSONS})
        for expected in ('SAST', 'SCA', 'DAST', 'RTO', 'RPO', '90 días', '10 caracteres', 'No aplica propuesto', 'acta de compromiso'):
            self.assertContains(page, expected)
        content = json.dumps(ACCEPTANCE, ensure_ascii=False).casefold()
        for forbidden in ('colgas', 'cinsa', 'cotranscol', 'vanti', 'cdtdegas', 'gmp250', 'csirt@'):
            self.assertNotIn(forbidden, content)
        self.assertContains(page, 'guides/expediente-aceptacion-industrial.md')
        self.assertContains(self.client.get('/ruta/entregar/'), '/ruta/vender/#matriz')
        self.assertContains(self.client.get('/'), 'mailto:ingeniero.oscargomez@gmail.com')
