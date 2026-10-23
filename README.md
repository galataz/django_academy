# Django con criterio

Academia pública para aprender a desarrollar proyectos Django profesionales. No requiere registro ni login. El proyecto guía es SensorHub, una plataforma de sensores independiente.

## Ruta práctica: vender, construir y entregar

La portada organiza el aprendizaje en **siete etapas con resultados revisables**: propuesta y aceptación industrial, solución en Azure, base Django, implementación reutilizable, protección y pruebas, publicación y operación/entrega.

Empieza en `/ruta/vender/` con la primera reunión y una matriz editable de requisitos y evidencias. Cada etapa incluye dos acciones sobre tu proyecto, temas en orden, ampliaciones y comprobación de su entrega. El catálogo de 78 lecciones está en `/biblioteca/`; la historia sigue en `/historia/`.

Las notas y el progreso anteriores se conservan. La matriz y las autoevaluaciones permanecen en el navegador y no certifican cumplimiento. Consulta [la organización y el alcance de la ruta](docs/ruta-practica.md).

## Arranque en Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py sync_catalog
python manage.py runserver
```

Abre http://127.0.0.1:8000. En Linux activa con `source .venv/bin/activate`.

## Actualizar una instalación anterior

Detén runserver. Reemplaza `academy/`, `templates/`, `static/`, `UTIL_LIB/`, `repoGenerico/` y `config/` con los de esta entrega; conserva tu entorno virtual. No sobrescribas db.sqlite3. Luego ejecuta migrate, sync_catalog y runserver. Esta ampliación conserva los IDs de los 61 temas anteriores y mantiene sus notas y progreso en el navegador. Si prefieres una instalación limpia, extrae el ZIP en otra carpeta y sigue el arranque inicial.

## Curso

78 lecciones en 11 unidades. Cada lección incluye problema, explicación, implementación paso a paso, código propio explicado, error habitual, ejercicio con solución y criterios de verificación. Los snippets completos se distinguen de esquemas con dependencias a implementar. El curso guía el diseño de SensorHub; no entrega una plataforma industrial completa lista para producción.

Temas: arquitectura modular; entornos; modelos UUID; relaciones; serializers; CQS; vistas genéricas; paginación; ORM; servicios; mixins; templates; frontend; cliente API; política de capacidades; permisos; sesiones y CSRF; identidad externa; auditoría; transacciones; UTIL_LIB; ingesta; timestamps; WebSockets; alarmas; outbox; decimación; exportaciones; pruebas; despliegue y proyecto final.

Interacciones: búsqueda, filtro por unidad, navegación, copiar código, notas y progreso local, exportación de cuaderno, explorador de capacidades y laboratorio API de conversión. No se envían notas al servidor. La ampliación conserva la clave del cuaderno y añade los nuevos temas al total del recorrido.

## Arquitectura de esta academia

`academy/views/queries/`: páginas y catálogo ORM.
`academy/views/commands/`: operación pública sin persistencia del laboratorio.
`repoGenerico/`: flujo común de lista paginada sobre ORM.
`UTIL_LIB/`: funciones puras de cálculo.
`academy/mixins.py`: composición cooperativa de contexto.
`academy/serializers.py`: contrato explícito de catálogo y entrada numérica.
`academy/content.json`: contenido educativo UTF-8 versionado.

El backend sincroniza los títulos y conceptos en Lesson mediante sync_catalog. El catálogo público se consulta con paginación y whitelist. Identidad, roles e ingesta se enseñan, no se activan como requisito para estudiar.

## Verificar

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

## Despliegue

Define DJANGO_SETTINGS_MODULE=config.settings.production, SECRET_KEY y ALLOWED_HOSTS. Ejecuta migrate, sync_catalog y collectstatic --noinput. Arranca gunicorn config.wsgi:application. WhiteNoise sirve estáticos. TLS debe estar configurado en el proxy; confía en cabeceras del proxy solo si son controladas. Para usar SQLite, configura almacenamiento persistente; para concurrencia elevada adapta DATABASES a PostgreSQL. GitHub Pages no ejecuta Django.

## Ampliación Azure y DevSecOps

Los temas 34–51 añaden identidades por entorno, convenciones de nombres, Zero Trust, Easy Auth y configuración, delegación B2B, MAU, integración MSAL, Azure IAM, slots/CI/ZIP Deploy, DNS y TLS, hardening Django, Application Insights/KQL, infraestructura LoRa y costos de VM, SMTP después del commit, SCA y trazabilidad de vulnerabilidades. Incluyen ejercicios, soluciones, comprobaciones y enlaces oficiales.

Los costos son escenarios educativos con supuestos explícitos; consulta tarifas y licencias vigentes. Los esquemas de identidad, SMTP e infraestructura enseñan otros proyectos y no activan autenticación ni crean recursos externos desde la academia. No se realizan envíos SMTP reales.

## PostgreSQL y mantenimiento de App Service

Los temas 52–57 explican gobierno de accesos, roles LOGIN/NOLOGIN, runtime/migrador/lector, aislamiento de bases, PUBLIC, propiedad, permisos de objetos existentes y futuros, pgAdmin, accesos temporales, psql y TLS. Los temas 58–61 cubren diagnóstico Kudu, cuota, cachés, clean deploy, retención, preservación del activo y reducción de plan.

Son laboratorios para tus proyectos: no cambian cuentas PostgreSQL, no borran archivos remotos ni cambian planes Azure desde esta academia. El curso continúa funcionando localmente con SQLite sin nuevas dependencias. Los bloques de consola indican dónde ejecutar cada comando y los cambios de mantenimiento requieren revisar el destino.

## Aprendizaje visual

La portada incluye un mapa de arquitectura y once ilustraciones de unidades. Cada uno de los 61 temas contiene una ilustración original, un mapa conceptual SVG de cuatro componentes y controles para destacar cada componente con su explicación. Sin JavaScript, el mapa y su alternativa textual siguen disponibles. Los diagramas se pueden descargar y ampliar sin perder calidad.

Los recursos se sirven localmente y no añaden dependencias al sitio. Edita las metáforas y relaciones en `scripts/build_visuals.py` y ejecuta `python scripts/build_visuals.py` para regenerar `academy/visuals.json`, los SVG y los mapas de plantilla. El generador usa solamente la biblioteca estándar de Python. Los esquemas son resúmenes didácticos: el texto de cada tema desarrolla sus condiciones y límites.

## Isla Django: aventura 3D

Abre `demo/isla_django.html` directamente en un navegador moderno para probar el juego sin instalar dependencias ni arrancar Django. Los enlaces al curso de esa demo apuntan al servidor local `http://127.0.0.1:8000/` y requieren que esté encendido. El juego en sí es autónomo.

Dentro de Django, entra en `/laboratorio/`. La portada y el tema 8 también incluyen el juego. Hay tres misiones CQS: consultar sensores, crear uno y rechazar una entrada inválida. Byte recorre cinco estaciones; cada parada plantea una decisión, explica su respuesta y muestra el código conceptual. La creación cambia el contador únicamente al confirmar la transacción simulada. Cada misión comienza con dos sensores.

La isla usa geometría 3D original, iluminación, sombras y animación, con Three.js 0.180.0 incluido localmente bajo licencia MIT (`static/THREE-LICENSE.txt`). No carga CDNs, no requiere cuenta y no envía datos. Los puntos y los sensores del juego viven en memoria; el progreso de las lecciones y las notas mantienen su almacenamiento anterior. El sonido es opcional y está apagado inicialmente.

Controles: toca una estación o usa los botones de viaje; arrastra para girar la cámara; rueda, pellizco o +/− para zoom. Tab y Enter permiten completar el juego con teclado. Movimiento reducido omite los desplazamientos animados. Si WebGL 2 no está disponible se ofrece acceso a la lección escrita.

### Actualizar una instalación existente

Copia `academy`, `config/urls.py`, `templates`, `static`, `game_src`, `scripts` y `demo`. Conserva tu entorno virtual, tu base de datos y tus settings locales. Reinicia `runserver` y recarga con Ctrl+F5. No hay cambios de modelos ni nuevas dependencias Python.

### Modificar el juego

El bundle está compilado; Node.js no es necesario para ejecutar Django ni la demo. Para editar la escena, modifica `game_src/world.js`; para cambiar misiones, `game_src/main.js`. Para recompilar:

```powershell
cd game_src
npm install
npm run build
cd ..
python scripts/export_game_demo.py
```

La experiencia 3D cubre el primer mundo de CQS. Las otras lecciones conservan sus ilustraciones y mapas SVG.

### Si el recuadro del juego aparece gris o bloqueado

La vista `GameView` permite incrustación del mismo origen con `xframe_options_sameorigin`. El resto del sitio conserva la política `DENY`. Si estás actualizando una versión anterior, sustituye `academy/views/queries/pages.py`, reinicia Django y recarga. No hace falta desactivar `XFrameOptionsMiddleware`.

## Tarjetas con miniaturas de Isla Django

Las 11 unidades y los 61 temas usan escenas 3D renderizadas en WebP, con la misma geometría, vegetación y paleta del juego. Las imágenes están en `static/cards/` y se cargan de forma diferida; no requieren WebGL para verse. El encabezado de cada lección comparte la ilustración de su tarjeta. Los mapas técnicos SVG se mantienen.

Para actualizar esta versión, copia `academy`, `templates` y `static`, reinicia Django y recarga con Ctrl+F5. No hay cambios de modelos ni nuevas dependencias Python.

Las imágenes ya están incluidas. Para regenerarlas, desde `game_src` ejecuta `npm install`, `npx playwright install chromium` y `npm run render:cards`. Las escenas se definen en `card-art.js` y la asociación con temas en `card-specs.json`.

## Ruta ampliada de entornos y despliegue

La unidad 8, **Azure y Django: configuración y despliegue**, recorre recursos/plan, IAM, variables, Gunicorn o Daphne, estáticos, preparación ZIP, PowerShell, Kudu con ZIP alojado, promoción y verificación. Los fundamentos añaden Git, PostgreSQL local y .env; la unidad de PostgreSQL añade restauración ensayada. Settings, apps, middleware, templates y MSAL se amplían donde corresponde.

Los temas conservan sus IDs y URLs para mantener notas y progreso. La posición visible sigue `order` en `academy/content.json`; la navegación anterior/siguiente y Continuar usan ese mismo recorrido. No se renumeran los datos guardados.

Los ejemplos empresariales son material educativo separado: no añaden MSAL, Docker, PostgreSQL ni python-dotenv como requisitos de ejecución de esta academia. Las capturas originales no se redistribuyen; los ejemplos usan nombres ficticios.

Después de actualizar, ejecuta `python manage.py sync_catalog` para que la API de catálogo muestre los 78 temas. Recarga el navegador con Ctrl+F5. El ZIP descargable contiene una carpeta envolvente para uso local: para Azure prepara deploy.zip con el layout y arranque definidos en la lección de empaquetado.

## Seguridad aplicada en los settings

`config/settings/base.py` declara HttpOnly de sesión, SameSite de sesión/CSRF, nombre del token CSRF, ventana deslizante de sesión, DENY para clickjacking, nosniff y Referrer-Policy. La academia sigue siendo pública y no activa sesiones ni autenticación por declarar estas opciones. El laboratorio conserva una excepción SAMEORIGIN para el iframe interno.

`production.py` exige SECRET_KEY y hosts explícitos, desactiva DEBUG, redirige a HTTPS y marca cookies Secure. Conserva la política de referencia: SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https'), SECURE_HSTS_SECONDS=31536000, SECURE_HSTS_INCLUDE_SUBDOMAINS=True y SECURE_HSTS_PRELOAD=True.

El entorno productivo debe terminar TLS correctamente, eliminar/sobrescribir X-Forwarded-Proto del cliente y evitar accesos directos que eludan el proxy. Todos los subdominios del alcance HSTS deben soportar HTTPS. PRELOAD no inscribe automáticamente el dominio en listas de navegadores. Estas condiciones se explican ajuste por ajuste en la lección productiva. No fuerces esta política HTTPS en development.py para HTTP local.

Comprueba el entorno productivo con `python manage.py check --deploy --settings=config.settings.production` y peticiones HTTPS reales. Los settings complementan validación, escape, permisos de API y mantenimiento de dependencias.


## Recorrido narrativo
Las 78 lecciones forman 11 capítulos conectados desde la necesidad del equipo
hasta una base replicable. `academy/story.json` agrupa los capítulos;
`content.json` conserva IDs estables y define el orden pedagógico y el contexto
narrativo de cada decisión. Las unidades siguen siendo filtros temáticos.
El proyecto final cierra ahora el recorrido. Notas y progreso conservan sus IDs.
El relato inicial adapta la experiencia proporcionada por el autor; SensorHub
es el caso didáctico y la secuencia no pretende ser una cronología literal.


Publicación manual: los temas 67–70 explican collectstatic y el layout anidado.
`python scripts/package_deploy.py --output ../deploy.zip` prepara un paquete
para Azure después de recolectar estáticos con el backend de producción.
El ZIP descargable del curso es para extraer en el PC; no es deploy.zip.
Los ejemplos de PostgreSQL/pool y MSAL no activan esos servicios en la academia pública.

Los temas 9 y 10 profundizan en repoGenerico: inventario, comparaciones antes/después,
hooks, contratos y paginación compartida. `repoGenerico/CONTRACT.md` y `AGENTS.md`
orientan la reutilización en futuras modificaciones humanas o asistidas por IA.


## Lectura continua del relato

Abre `/historia/` o **Leer la historia completa** en la portada. El prólogo
presenta el recorrido; 78 escenas desarrollan las decisiones del equipo en
11 capítulos, desde el origen hasta la reutilización de la base.
Cada escena enlaza con su práctica técnica. El mismo texto abre la lección
correspondiente; ya no se presenta como tres casillas de necesidad/decisión/resultado.

La fuente editorial es `academy/narrative.json`, leída explícitamente como UTF-8.
Sus claves son los IDs estables de las lecciones; el orden proviene del catálogo
y de `academy/story.json`. Para actualizar esta entrega, copia también `config/`
(por la nueva ruta), `academy/`, `templates/` y `static/`. La política de seguridad
se conserva. Notas, progreso y ejemplos técnicos mantienen sus identificadores.


## Aceptación industrial: requisitos, evidencias y compromisos

Abre `/tema/78/`. La nueva lección se integra antes del proyecto final y en el
relato continuo. Desarrolla 22 apartados y una matriz de 29 familias de controles,
con ejemplos de brechas, responsabilidades y pruebas ante TI, infraestructura y
seguridad. Los números contractuales se presentan como ejemplos que requieren
acuerdo para cada servicio. No se declara cumplimiento del proyecto del cliente.

Incluye un modelo didáctico descargable de expediente y acta de compromiso:
`static/guides/expediente-aceptacion-industrial.md`. Los documentos originales,
sus nombres de clientes y sus referencias confidenciales no forman parte del ZIP.

Para actualizar esta versión: reemplaza `academy`, `templates` y `static` y
actualiza este README. Conserva tu base de datos y tus variables de entorno.
Ejecuta `python manage.py sync_catalog`, reinicia y recarga con Ctrl+F5.
