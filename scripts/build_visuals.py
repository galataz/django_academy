"""Genera el vocabulario SVG original y los mapas semánticos del curso.
No requiere paquetes externos. Edita SPECS y ejecuta python scripts/build_visuals.py.
"""
import json, html, textwrap, base64
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'static/visuals'
OUT.mkdir(exist_ok=True)
SPECS = [
('Del plano al taller','flow','brief:Requisitos:Define problema y restricciones|map:Módulos:Separa responsabilidades|db:Modelo:Representa reglas del dominio|check:Criterios:Comprueba el comportamiento'),
('Una mesa de trabajo reproducible','flow','tool:Entorno:Aísla dependencias|folder:Proyecto:Crea estructura y configuración|code:Dependencias:Declara el stack|check:Arranque:Verifica instalación limpia'),
('Un proyecto, tres configuraciones','branch','gear:Base:Comparte ajustes comunes|tool:DEV:Facilita desarrollo local|check:TEST:Controla pruebas aisladas|cloud:PROD:Exige secretos y hosts'),
('Módulos con conexiones claras','branch','folder:Apps:Delimita responsabilidades|db:Modelos:Gestionan persistencia|code:Servicios:Coordinan casos de uso|screen:Vistas:Adaptan HTTP al dominio'),
('Un molde para identidades únicas','branch','blocks:Base abstracta:Comparte campos comunes|key:UUID:Identidad estable|db:Sensor:Hereda la base|db:Estación:Hereda la base'),
('Piezas que encajan con reglas','flow','db:Estación:Agrupa sensores|sensor:Sensor:Pertenece a una estación|rule:Restricción:Protege integridad|check:Base de datos:Hace cumplir la regla'),
('Una aduana para los datos','flow','packet:Entrada:Datos sin confiar|filter:Serializer:Valida forma y valores|code:Datos válidos:Llegan al caso de uso|packet:Salida:Contrato explícito de respuesta'),
('Dos carriles para dos intenciones','cqs','packet:Petición:Expresa una intención|search:Query:Consulta sin cambiar estado|code:Command:Ejecuta una operación|db:Estado:Se consulta o modifica según carril'),
('Un molde con puntos de extensión','branch','blocks:Vista genérica:Define el flujo común|db:Queryset:Selecciona los datos|filter:Serializer:Define la representación|packet:Respuesta:Conserva el contrato compartido'),
('Una ventana sobre un catálogo','flow','search:Parámetros:Busqueda, página y orden|shield:Validación:Limita rango y campos|db:Consulta:Filtra antes de paginar|screen:Página:Muestra un subconjunto ordenado'),
('Traer las piezas en pocos viajes','flow','screen:Lista:Necesita objetos relacionados|db:ORM:Planifica consulta y relaciones|blocks:Precarga:Evita viajes por cada fila|meter:Medición:Comprueba cantidad de consultas'),
('El coordinador del caso de uso','flow','screen:Vista:Adapta la petición|filter:Validación:Comprueba entrada|tool:Servicio:Coordina reglas y persistencia|db:Repositorio:Accede al estado'),
('Una cadena cooperativa de trabajo','flow','blocks:Vista compuesta:Combina comportamiento|tool:Mixin:Añade una responsabilidad|route:super():Continúa según MRO|screen:Contexto:Conserva lo aportado por las bases'),
('Una página construida con piezas','branch','screen:Template base:Define estructura compartida|blocks:Includes:Reutilizan fragmentos|packet:Contexto:Entrega datos de la vista|screen:Página:Renderiza la composición'),
('Un panel con estado visible','cycle','screen:Interacción:Usuario ejecuta acción|gear:Estado:Representa situación actual|code:Módulo:Aplica transición explícita|screen:Render:Actualiza interfaz desde estado'),
('Un mensajero para todas las llamadas','flow','screen:Frontend:Solicita una operación|route:Cliente API:Centraliza transporte|packet:Respuesta:Éxito o error estructurado|shield:Manejo:Presenta el resultado coherentemente'),
('Una llave por capacidad','branch','person:Actor:Identidad del ejemplo|rule:Política:Relaciona roles y capacidades|key:Capacidad:Permite una acción específica|shield:Decisión:Autoriza o deniega con alcance'),
('La puerta real está en el servidor','flow','screen:Interfaz:Muestra acciones permitidas|packet:Petición:Puede fabricarse fuera de la UI|shield:API:Verifica identidad y permiso|db:Objeto:Comprueba alcance de negocio'),
('Controles en el recorrido HTTP','flow','screen:Navegador:Envía cookie y petición|shield:CSRF:Verifica escritura del navegador|route:Middleware:Prepara contexto y controles|code:Vista:Ejecuta tras las verificaciones'),
('Identidad externa, permisos propios','flow','person:Usuario:Inicia flujo de identidad|key:Entra / MSAL:Adquiere contexto autenticado|filter:Adaptador:Resuelve identidad verificada|rule:Política local:Evalúa capacidades y objetos'),
('Un registro de cambios con contexto','flow','person:Actor:Ejecuta una acción|tool:Servicio:Aplica el cambio autorizado|db:Estado:Guarda el resultado|brief:Auditoría:Conserva quién, qué y cuándo'),
('Una operación que confirma una vez','flow','packet:Solicitud:Incluye identidad de operación|key:Idempotencia:Detecta intentos repetidos|db:Transacción:Coordina cambios atómicos|check:Resultado:Confirma o revierte el conjunto'),
('Una herramienta con entrada y salida','flow','meter:Valor:Incluye unidad de entrada|filter:Validación:Comprueba rango y tipo|tool:Función pura:Transforma sin efectos externos|meter:Resultado:Expresa la unidad destino'),
('Del dispositivo al dato validado','flow','sensor:Dispositivo:Produce una medición|key:Credencial técnica:Identifica al emisor|filter:Ingesta:Valida contrato y duplicados|db:Medición:Persiste el dato aceptado'),
('Una medición conserva su contexto','branch','meter:Medición:Valor original observado|clock:Tiempo:Identifica instante y zona|gear:Calibración:Versión aplicada al valor|db:Snapshot:Permite interpretar el histórico'),
('Una conexión viva con permisos','flow','screen:Cliente:Abre conexión persistente|route:ASGI:Gestiona conexión y eventos|shield:Consumer:Verifica acceso y alcance|packet:Canal:Distribuye eventos autorizados'),
('La alarma cambia por eventos','cycle','check:Normal:Condición dentro de umbral|alert:Activa:Evento activa la alarma|person:Reconocida:Operador acusa recibo|check:Resuelta:Condición vuelve a normalidad'),
('Dos trabajos unidos por un evento','flow','tool:Servicio:Decide cambio de negocio|db:Commit + outbox:Persiste estado y trabajo|gear:Worker:Procesa trabajo pendiente|mail:Efecto:Notifica con control de reintento'),
('Muchos puntos, una vista legible','flow','db:Histórico:Conserva muestras completas|filter:Filtros:Elige intervalo y sensores|chart:Decimación:Reduce puntos para presentar|screen:Gráfico:Expone tendencia y detalle'),
('Una salida con un contrato seguro','flow','person:Solicitante:Define reporte requerido|shield:Alcance:Restringe datos autorizados|db:Consulta:Obtiene valores exportables|brief:CSV / reporte:Entrega formato controlado'),
('Una prueba observa comportamiento','flow','brief:Escenario:Define estado y objetivo|packet:Acción:Ejecuta comportamiento real|check:Resultado:Comprueba efecto esperado|shield:Caso negativo:Verifica que lo inválido falle'),
('Publicar y comprobar el servicio','flow','folder:Artefacto:Versionado y reproducible|cloud:Destino:Configuración y secretos|check:Salud:Verifica servicio y dependencias|meter:Observación:Detecta fallos y consumo'),
('El taller completo de SensorHub','branch','screen:Experiencia web:Consulta y acciones|tool:Casos de uso:Aplican reglas y capacidades|db:Datos:Catálogo e históricos|sensor:Telemetría:Ingesta, eventos y alarmas'),
('Dos entornos, dos juegos de llaves','compare','tool:DEV:Identidad de laboratorio|key:Client ID DEV:Credenciales y callbacks propios|cloud:PROD:Identidad productiva|key:Client ID PROD:Permisos y secretos separados'),
('Un nombre legible, un ID estable','flow','brief:Convención:Tipo, entorno y servicio|key:Identificador:Vincula el objeto real|person:Propietario:Responde por el ciclo de vida|clock:Revisión:Renueva, verifica o retira'),
('Verificar en cada límite de confianza','flow','key:Identidad:Verifica quién solicita|shield:Asignación:Controla ingreso corporativo|rule:Permiso:Autoriza acción y objeto|brief:Evidencia:Registra decisiones sensibles'),
('Autenticar antes de llegar a Django','flow','person:Cliente:Solicita acceso|shield:Easy Auth:Controla autenticación en plataforma|key:Entra ID:Autentica al usuario|code:Django:Recibe contexto y evalúa negocio'),
('Conectar proveedor y destino correcto','flow','cloud:App Service:Selecciona recurso y entorno|key:Registro:Configura tenant y Client ID|route:Callback:Coincide con URI registrada|check:Pruebas:Acceso válido y denegaciones'),
('Delegar facultades por separado','branch','person:Delegado:Responsabilidad acordada|key:Invitación B2B:Facultad de directorio|rule:Acceso a app:Membresías autorizadas|gear:Configuración:Propiedad con alcance revisado'),
('Contar personas, no cada ingreso','flow','person:Ingresos del mes:Eventos de autenticación|filter:Usuarios únicos:Deduplica según medidor|meter:MAU cobrable:Aplica umbral confirmado|brief:Estimación:Tarifa verificada y extras'),
('Un adaptador entre identidad y dominio','flow','key:Claims verificadas:No son JSON sin validar|filter:Adaptador:Construye actor estable|rule:Capacidades:Mapea roles conocidos|shield:Objeto:Evalúa pertenencia y alcance'),
('Permisos cloud con un alcance concreto','flow','person:Principal:Persona o identidad técnica|key:Rol Azure:Conjunto de acciones permitidas|map:Scope:Recurso que se administra|check:Prueba:Confirma permitidos y denegados'),
('Promover un artefacto comprobado','flow','folder:Artefacto:Vinculado al commit|cloud:Staging / destino:Publica según estrategia|check:Validación:Salud, datos y funciones|route:Promoción:Swap o deploy con reversión'),
('Un nombre llega a un servicio seguro','flow','screen:Dominio:Nombre público de la app|route:DNS:Resuelve y verifica propiedad|shield:TLS:Certificado y binding válidos|code:Django:Hosts, CSRF y enlaces canónicos'),
('Controles entre navegador y aplicación','flow','screen:Cliente:Usa HTTPS|shield:Proxy confiable:Controla cabeceras de transporte|gear:Settings:Hosts, secretos y seguridad|check:Verificación:Prueba configuración efectiva'),
('Observar sin enviar ruido ilimitado','flow','code:Aplicación:Emite señales necesarias|filter:Filtros / sampling:Reduce volumen según mecanismo|db:Workspace:Almacena telemetría|meter:Consumo:Analiza volumen, retención y alertas'),
('Conectividad, cómputo y recuperación','branch','sensor:Gateways:Emiten según protocolo del stack|shield:Red y NSG:Limitan rutas y orígenes|cloud:VM LoRa:Ejecuta los servicios|db:Estado y backup:Persistencia y restauración'),
('Ahorrar sin borrar lo recuperable','branch','meter:Costo observado:Separa rubros reales|cloud:Cómputo:Evalúa desasignación y disponibilidad|db:Discos / backup:Persisten y siguen costando|check:Verificación:Comprueba ahorro y recuperación'),
('El correo sale después de confirmar','flow','tool:Evento de negocio:Cambio dentro de transacción|db:Commit:Confirma o descarta callback|mail:on_commit:Envía sin garantía de reintento|gear:Outbox opcional:Entrega durable si es necesaria'),
('Revisar lo que realmente está instalado','flow','folder:Inventario:Artefacto y versiones resueltas|search:Advisories:Comprueba versiones afectadas|shield:Aplicabilidad:Evalúa exposición y riesgo|tool:Corrección:Prueba cambio y despliegue'),
('Un hallazgo se cierra con evidencia','flow','alert:Hallazgo:Aviso y versión confirmados|brief:Decisión:Riesgo, responsable y plazo|tool:Cambio:Actualiza y prueba artefacto|check:Cierre:Verifica versión en destino'),
('Tres capas de gobierno distintas','branch','person:Responsabilidad:Define tarea y duración|cloud:Azure RBAC:Opera recurso cloud|db:Roles SQL:Controlan conexión y objetos|rule:Política Django:Autoriza negocio'),
('Cada oficio tiene su llave','branch','db:Base de datos:Objetos y propietarios|code:Runtime:Opera datos concedidos|tool:Migrador:Controla estructura autorizada|search:Lector:Consulta sin DML ni DDL'),
('Trabajar en compartimentos separados','compare','tool:DEV:Cuenta y datos de prueba|db:Base DEV:Objetos de su desarrollador|cloud:PROD:Cuenta de runtime separada|db:Base PROD:CONNECT y permisos acotados'),
('Quien crea define permisos futuros','flow','tool:Rol migrador:Creador efectivo de objetos|key:Defaults:Reglas para objetos futuros|db:Nueva tabla:Recibe ACL al crearse|check:Runtime / lector:Prueban permisos concedidos'),
('Una interfaz no es la barrera de acceso','compare','screen:pgAdmin:Organiza conexiones y árbol|filter:DB restriction:Filtra vista, no protege acceso|db:PostgreSQL:Evalúa roles y privilegios|shield:Revocación:Comprueba membresías y sesiones'),
('Verificar destino antes de operar','flow','route:psql + TLS:Conecta al servidor verificado|key:Identidad efectiva:Usuario y rol actuales|search:Inspección:ACL, defaults y propietarios|check:Pruebas:Acciones permitidas y denegadas'),
('Medir antes de tocar archivos','flow','alert:Error de cuota:Identifica operación y destino|search:Kudu:Inspecciona entorno y montajes|meter:Medición:Localiza directorio que creció|brief:Diagnóstico:Clasifica datos y regenerables'),
('Código y caché viven en sitios distintos','compare','folder:Deploy:Reemplaza artefacto destino|code:wwwroot:Contenido publicado según método|tool:Build:Descarga herramientas y dependencias|db:Caché:Puede persistir fuera del destino'),
('Conservar, revisar y limpiar lo necesario','flow','meter:Inventario:Mide rutas y causas|shield:Preservación:Protege datos y evidencia|filter:Candidatos:Lista regenerables autorizados|check:Mantenimiento:Mide de nuevo y prueba build'),
('El ahorro debe conservar requisitos','flow','cloud:Plan actual:Apps y funciones compartidas|meter:Destino F1:Cuota y soporte comprobados|filter:Preparación:Reduce uso con margen|check:Validación:Prueba cambio y reversión prevista'),

]
assert len(SPECS)==61
SPECS += [('El taller compartido', 'flow', 'folder:Clonar:Copia el proyecto versionado|route:Rama:Aísla una propuesta|check:Verificar:Prueba y revisa cambios|packet:Entregar:Publica para revisión'), ('El panel de configuración', 'flow', 'folder:Archivo local:Define valores de práctica|gear:Cargador:Lee antes de importar base|rule:Tipos:Convierte y valida entradas|code:Django:Usa configuración efectiva'), ('La casa y su terreno', 'branch', 'cloud:App Service:Ejecuta la aplicación web|blocks:Plan:Define capacidad compartida|folder:Grupo:Organiza recursos|key:Entra:Registra identidad aparte'), ('La caja de variables', 'flow', 'brief:Contrato:Define nombres y tipos|key:Valores:Separa secretos por entorno|cloud:Azure:Inyecta al proceso|check:Verificación:Revisa sin exponer claves'), ('Dos puertas de entrada', 'compare', 'screen:HTTP:Petición web convencional|gear:Gunicorn:Importa aplicación WSGI|route:ASGI:HTTP y tiempo real|gear:Daphne:Importa aplicación ASGI'), ('La fábrica de estáticos', 'flow', 'folder:Fuentes:CSS JS e imágenes|tool:collectstatic:Reúne archivos del build|packet:STATIC_ROOT:Conserva salida generada|cloud:Servidor:Entrega recursos estáticos'), ('La maleta del despliegue', 'flow', 'folder:Commit:Identifica código revisado|rule:Inventario:Excluye secretos y venv|packet:ZIP:Conserva raíz correcta|check:Hash:Identifica el artefacto'), ('La consola de publicación', 'flow', 'key:Operador:Inicia sesión en Azure|search:Destino:Comprueba app y suscripción|packet:Publicación:Envía paquete revisado|check:Salud:Comprueba arranque real'), ('El muelle de Kudu', 'flow', 'packet:deploy.zip:Paquete manual preparado|cloud:Kudu:Usa una operación de despliegue|tool:Build Linux:Instala dependencias|check:Validación:Revisa logs y resultado'), ('El ciclo de una entrega', 'cycle', 'code:Desarrollar:Cambia y prueba localmente|packet:Publicar:Entrega artefacto identificado|chart:Observar:Comprueba salud y negocio|tool:Aprender:Ajusta o recupera y repite'), ('Una base para practicar', 'flow', 'blocks:Contenedor:Aísla el laboratorio|db:Volumen:Conserva datos locales|key:Roles:Separa tareas y permisos|code:Django:Conecta con usuario limitado'), ('La prueba de recuperación', 'flow', 'db:Origen:Identifica alcance de copia|packet:Backup:Protege el archivo generado|db:Restauración:Usa una base aislada|check:Ensayo:Valida datos y acceso')]
SPECS += [
 ('Las defensas de cada petición','flow','screen:Petición:Entrada y contexto de confianza|shield:Middleware:Aplica los controles comunes|key:Cookies:Define acceso y envío|check:Respuesta:Comprueba cabeceras y contrato'),
 ('El perímetro HTTPS','flow','cloud:Proxy TLS:Protege transporte externo|shield:Django:Reconoce protocolo confiable|key:Cookies Secure:Restringe envío a HTTPS|check:HSTS:Comprueba alcance y duración')]
SPECS += [
('Conexiones con un presupuesto','flow','screen:Procesos:Cada worker usa su pool|blocks:Pool:Presta conexiones con límite|db:PostgreSQL:Recibe consultas y transacciones|meter:Medición:Observa espera y conexiones'),
('Capacidad que se comprueba','flow','sensor:Carga:Cuatro IoT y usuarios|db:Flexible Server:Separa CPU memoria y disco|meter:Métricas:Mide créditos y latencia|brief:Decisión:Cotiza y ajusta con evidencia'),
]
assert len(SPECS) == 77
COLORS=['#437e69','#d48554','#4b7d9c','#a177a0','#76894c','#4c9290','#587ba0','#ce8655','#719466','#667fa6','#b8875a']
# Símbolos diseñados para el curso; trazo común y geometría editorial.
ICONS={
'screen':'<rect x="10" y="14" width="80" height="54" rx="5"/><path d="M38 85h24M50 68v17"/><path d="M20 25h26m-26 12h48m-48 12h31"/>',
'db':'<ellipse cx="50" cy="22" rx="32" ry="12"/><path d="M18 22v56c0 16 64 16 64 0V22M18 40c0 16 64 16 64 0M18 58c0 16 64 16 64 0"/>',
'key':'<circle cx="33" cy="34" r="20"/><circle cx="33" cy="34" r="6"/><path d="m47 48 36 36h12V71H83V59H71L61 49"/>',
'shield':'<path d="m50 8 34 13v30c0 20-18 33-34 41C34 84 16 71 16 51V21Z"/><path d="m32 49 12 13 25-29"/>',
'folder':'<path d="M10 28V18h31l10 12h39v53H10Z"/><path d="M10 37h80M24 50h31m-31 12h48"/>',
'code':'<rect x="8" y="14" width="84" height="72" rx="7"/><path d="m35 37-15 13 15 13m30-26 15 13-15 13m-11-33-8 40"/>',
'blocks':'<path d="M12 14h33v33H12Zm43 0h33v33H55ZM12 57h33v33H12Zm43 0h33v33H55Z"/><path d="M23 27h11m33 0h11M23 72h11m33 0h11"/>',
'gear':'<path d="m42 8 16 0 4 15 14-5 12 12-6 14 14 6-2 16-16 3 2 15-14 9-12-9-11 11-15-7 1-16-16-1-4-16 13-9-8-13 10-13 15 4Z"/><circle cx="50" cy="51" r="15"/>',
'person':'<circle cx="50" cy="26" r="15"/><path d="M20 86V64c0-23 60-23 60 0v22M34 57v29m32-29v29M40 26h0m20 0h0"/>',
'packet':'<rect x="17" y="13" width="66" height="76" rx="5"/><path d="M30 28h40M30 43h18m-18 14h40m-40 14h28"/>',
'search':'<circle cx="42" cy="42" r="28"/><path d="m63 63 26 26M28 36h27m-27 13h18"/>',
'filter':'<path d="M8 15h84L61 51v32l-22 8V51Z"/><path d="M23 28h54"/>',
'meter':'<path d="M10 72a40 40 0 0 1 80 0Z"/><path d="m50 70 21-28M25 55l-7-7m61 6 8-6M50 38v-9"/><circle cx="50" cy="70" r="5"/>',
'sensor':'<rect x="28" y="42" width="44" height="48" rx="8"/><circle cx="50" cy="64" r="8"/><path d="M40 80h20M50 42V28m-14 0a18 18 0 0 1 28 0M22 17a35 35 0 0 1 56 0"/>',
'cloud':'<path d="M22 70C0 68 5 37 25 37 25 7 74 4 76 36c27-3 32 34 8 34Z"/><path d="M36 55h28M43 70v20m14-20v20"/>',
'check':'<circle cx="50" cy="50" r="38"/><path d="m27 50 16 18 30-36"/>',
'alert':'<path d="m50 10 43 76H7Z"/><path d="M50 34v25m0 12h0"/>',
'mail':'<rect x="9" y="23" width="82" height="56" rx="5"/><path d="m12 28 38 30 38-30M12 75l25-25m51 25L64 50"/>',
'chart':'<path d="M13 12v74h77M27 69l17-24 17 10 23-31"/><path d="M23 20h16"/>',
'brief':'<rect x="18" y="18" width="64" height="73" rx="4"/><path d="M36 9h28v19H36ZM30 42h38m-38 14h38m-38 14h25"/>',
'route':'<path d="M12 78V28h62M62 16l13 12-13 12M87 23v50H27m10-12L25 73l12 12"/>',
'clock':'<circle cx="50" cy="50" r="38"/><path d="M50 24v28l20 12M50 13v5m0 64v5M13 50h5m64 0h5"/>',
'rule':'<rect x="12" y="14" width="76" height="73" rx="5"/><path d="m23 35 6 6 10-13m-16 31 6 6 10-13M49 34h26M49 59h26"/>',
'map':'<path d="m7 24 28-13 30 13 28-13v65L65 89 35 76 7 89ZM35 11v65m30-52v65"/>',
 'tool':'<path d="M63 10c-25-6-40 19-26 37L9 76l15 15 29-29c21 11 43-7 36-29L72 50 53 31Z"/>'}
def esc(s):return html.escape(str(s),quote=True)
def symbols():
 return '<defs>'+''.join(f'<symbol id="{k}" viewBox="0 0 100 100"><g fill="#fbf8ef" stroke="#293c37" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">{v}</g></symbol>' for k,v in ICONS.items())+'</defs>'
def icon(name,x,y,size=62):return f'<use href="#{name}" x="{x}" y="{y}" width="{size}" height="{size}"/>'
def svg(body,w,h,title,desc):return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{esc(title)}</title><desc id="desc">{esc(desc)}</desc>{symbols()}{body}</svg>'
def txt(x,y,s,size=18,anchor='start',fill='#293c37',weight=600):return f'<text x="{x}" y="{y}" font-family="DejaVu Sans, sans-serif" font-size="{size}" text-anchor="{anchor}" fill="{fill}" font-weight="{weight}">{esc(s)}</text>'
def wrap(x,y,s,width=26,size=15,anchor='middle',fill='#66786e'):
 return ''.join(txt(x,y+i*(size+6),line,size,anchor,fill,400) for i,line in enumerate(textwrap.wrap(s,width)))
def vignette(n,nodes,color,caption):
 # Small original workshop illustration, no text needed for card recognition.
 b=f'<path d="M26 124 169 53l174 80-141 87Z" fill="{color}" opacity=".12"/><path d="m26 124 176 80 141-71M26 124v13l176 81 141-72v-13M202 204v14" fill="none" stroke="#293c37" stroke-width="2"/>'
 b+=f'<path d="M91 60h120v106H91Z" fill="#fbf8ef" stroke="#293c37" stroke-width="2.5"/><path d="M104 76h63" stroke="{color}" stroke-width="6"/>'
 b+=icon(nodes[0]['icon'],118,88,65)
 b+=f'<circle cx="272" cy="105" r="44" fill="{color}" opacity=".16"/>'+icon(nodes[-1]['icon'],242,74,62)
 # Technician with tablet, distinctive neutral original character.
 b+='<circle cx="62" cy="106" r="13" fill="#fbf8ef" stroke="#293c37" stroke-width="2.5"/><path d="M48 102q13-20 28 0M59 110h7M51 126l-7 41m27-41 8 36M52 150l-7 36m19-36 8 36" fill="none" stroke="#293c37" stroke-width="3" stroke-linecap="round"/>'
 b+=f'<path d="m51 124 20 0 5 28-30 0Z" fill="{color}" stroke="#293c37" stroke-width="2.5"/><path d="m73 135 20 3" stroke="#293c37" stroke-width="3"/><rect x="81" y="127" width="22" height="27" rx="3" fill="#fbf8ef" stroke="#293c37" stroke-width="2"/>'
 b+='<path d="M213 84q30-35 64-26" fill="none" stroke="#293c37" stroke-width="2" stroke-dasharray="4 5"/><path d="m271 52 8 6-7 6" fill="none" stroke="#293c37" stroke-width="2"/>'
 b+=txt(315,206,f'{n:02}',18,fill=color)
 return svg(b,370,235,caption,'Ilustración de taller: '+nodes[0]['label']+' y '+nodes[-1]['label']+'. La relación técnica se explica en el mapa de la lección.')
# Reuse the original island miniatures; embedded bytes keep downloads self-contained.
ART = dict(screen=15, db=52, key=53, person=34, shield=36, sensor=24,
 cloud=43, tool=58, gear=3, folder=28, brief=30, packet=28, code=9,
 blocks=4, chart=46, meter=48, search=10, filter=10, check=31,
 rule=31, mail=49, clock=25, route=8, map=1, alert=27)
def island(name,x,y,w,h):
 asset=ROOT/f'static/cards/lesson-{ART[name]:02}.webp'
 data=base64.b64encode(asset.read_bytes()).decode('ascii')
 return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" href="data:image/webp;base64,{data}"/>'
def tile(node,x,y,w,h,color,index):
 return (f'<g id="node-{index}" class="visual-node"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="#fffdf8" stroke="#d5ddd2" stroke-width="1.5"/>'
  +island(node['icon'],x+12,y+8,w-24,210)
  +txt(x+22,y+32,f'{index:02}',15,fill=color)
  +wrap(x+w/2,y+245,node['label'],width=26,size=22,fill='#293c37')
  +wrap(x+w/2,y+295,node['detail'],width=34,size=17)+'</g>')
def connector(x,y,X,Y,w,h):
 if y==Y:
  return f'M{x+w+5 if X>x else x-5} {y+h/2}L{X-12 if X>x else X+w+12} {Y+h/2}'
 sy=y+h+5 if Y>y else y-5;ey=Y-12 if Y>y else Y+h+12
 middle=(sy+ey)/2
 return f'M{x+w/2} {sy}C{x+w/2} {middle} {X+w/2} {middle} {X+w/2} {ey}'
def map_svg(body,w,h,title,desc):
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{esc(title)}</title><desc id="desc">{esc(desc)}</desc>{body}</svg>'
def graph(n,nodes,kind,color,title):
 pos=[(30,30),(550,30),(30,465),(550,465)]
 edges={'flow':[(0,1),(1,2),(2,3)],'cycle':[(0,1),(1,2),(2,3),(3,0)],'branch':[(0,1),(0,2),(0,3)],'compare':[(0,1),(2,3)],'cqs':[(0,1),(0,2),(1,3),(2,3)]}[kind]
 if n==49: edges=[(0,1),(1,2),(1,3)]
 if n==37: edges=[(0,1),(1,2),(2,1),(1,3)]
 b='<rect width="1000" height="835" rx="28" fill="#f6f4eb"/>'
 b+=f'<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="m1 1 5 3-5 3" fill="none" stroke="{color}" stroke-width="1.5"/></marker></defs>'
 for i,j in edges:
  d=connector(*pos[i],*pos[j],420,340)
  b+=f'<path d="{d}" fill="none" stroke="{color}" stroke-width="3" marker-end="url(#arrow)"/>'
 for i,(node,(x,y)) in enumerate(zip(nodes,pos)):
  b+=tile(node,x,y,420,340,color,i+1)
 return map_svg(b,1000,835,title,'; '.join(f"{i+1}. {v['label']}: {v['detail']}" for i,v in enumerate(nodes)))
lessons=json.loads((ROOT/'academy/content.json').read_text(encoding='utf-8'))
visuals={}
for lesson in lessons:
 metaphor,kind,raw = SPECS[lesson['id']-1]
 nodes=[dict(zip(['icon','label','detail'],part.split(':',2))) for part in raw.split('|')]
 color=COLORS[lesson['unit']-1];n=lesson['id']
 relation={'flow':'Las flechas resumen el recorrido conceptual. Los controles y dependencias se detallan debajo.','branch':'Las flechas muestran responsabilidades relacionadas; no representan un orden obligatorio de ejecución.','compare':'Cada carril muestra un ámbito distinto. Compara sus responsabilidades antes de unir sus configuraciones.','cycle':'Las flechas muestran transiciones del modelo. Los eventos y guardas determinan cuáles están permitidas.','cqs':'La intención separa consulta y comando. El comando cambia estado; la consulta lo lee.'}[kind]
 # Custom technical corrections to avoid turning alternatives into chronological steps.
 if n==37:relation='El flujo de autenticación sale a Entra y vuelve a la plataforma antes de Django. El mapa resume responsabilidades, no el detalle de redirecciones HTTP.'
 if n==49:relation='on_commit se usa después del commit. Outbox es una alternativa para entrega durable, no un paso automático que siga a cada correo.'
 if n==27:relation='Los eventos pueden activar, reconocer y resolver una alarma; el flujo concreto define retornos y transiciones adicionales. Este mapa es un modelo didáctico.'
 visuals[str(n)]=dict(title=metaphor,color=color,kind=kind,nodes=nodes,caption=relation,illustration=f'visuals/lesson-{n:02}-scene.svg',diagram=f'visuals/lesson-{n:02}-map.svg')
 (OUT/f'lesson-{n:02}-scene.svg').write_text(vignette(n,nodes,color,metaphor),encoding='utf-8')
 (OUT/f'lesson-{n:02}-map.svg').write_text(graph(n,nodes,kind,color,metaphor),encoding='utf-8')
 # Partial trusted SVG compiled locally, no user-provided markup is marked safe.
 (ROOT/f'templates/academy/visual_maps/map_{n}.html').parent.mkdir(exist_ok=True)
 (ROOT/f'templates/academy/visual_maps/map_{n}.html').write_text(graph(n,nodes,kind,color,metaphor),encoding='utf-8')
(ROOT/'academy/visuals.json').write_text(json.dumps(visuals,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Global architecture map, six responsibilities with meaningful connections.
nodes=[('screen','Frontend','Interfaz y estado',30,30),('shield','Acceso','Identidad y capacidades',435,30),('sensor','Dispositivos','Ingesta validada',840,30),('tool','Casos de uso','Reglas, comandos y consultas',30,465),('db','Persistencia','Catálogo, historial y outbox',435,465),('cloud','Operación','Despliegue y observabilidad',840,465)]
b='<rect width="1200" height="835" rx="28" fill="#f1f0e5"/><defs><marker id="global-arrow" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="m1 1 6 3-6 3" fill="none" stroke="#437e69" stroke-width="1.5"/></marker></defs>'
for i,j in [(0,3),(1,3),(2,4),(3,4),(5,4)]:
 d=connector(*nodes[i][3:],*nodes[j][3:],330,340)
 b+=f'<path d="{d}" fill="none" stroke="#437e69" stroke-width="3" marker-end="url(#global-arrow)"/>'
for i,(k,label,detail,x,y) in enumerate(nodes):
 b+=tile(dict(icon=k,label=label,detail=detail),x,y,330,340,'#437e69',i+1)
(OUT/'course-map.svg').write_text(map_svg(b,1200,835,'SensorHub: arquitectura de conjunto','Frontend y acceso se relacionan con los casos de uso. Dispositivos alimentan persistencia a través de ingesta validada. Casos de uso acceden a persistencia. Operación despliega y observa estos componentes; las flechas indican relaciones, no todas las llamadas.'),encoding='utf-8')
# Unit illustrations are original course images reused as chapter identities.
for unit in range(1,12):
 first=next(l for l in lessons if l['unit']==unit)
 (OUT/f'unit-{unit:02}.svg').write_text((OUT/f"lesson-{first['id']:02}-scene.svg").read_text(encoding='utf-8'),encoding='utf-8')
print(f'Generated {len(lessons)} lesson maps and course architecture.')
