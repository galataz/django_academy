# De la propuesta a la entrega industrial

La portada presenta siete entregas. El catálogo de 78 lecciones queda disponible como biblioteca de consulta, y el relato conserva su cronología para lectura opcional. La navegación técnica sigue la etapa en curso; al terminar una etapa devuelve a su entrega en lugar de enviar al usuario a un tema de otra unidad.

| Etapa | Pregunta | Resultado revisable |
| --- | --- | --- |
| 1. Propuesta | ¿Qué exigirá el cliente antes de aceptar? | Alcance, matriz de requisitos, brechas y costo de cumplir |
| 2. Solución en Azure | ¿Qué recursos y responsabilidades necesito? | Arquitectura, inventario y presupuesto por ambiente |
| 3. Base Django | ¿Otro compañero puede reproducir el arranque? | Entorno, repositorio, settings, modelos y configuración |
| 4. Implementación | ¿Cómo crece sin duplicar controladores? | CQS, repoGenerico, contrato API, interfaz y flujo de datos |
| 5. Protección y pruebas | ¿Puedo demostrar permisos y seguridad? | Matriz de permisos, auditoría e informes por versión |
| 6. Publicación | ¿El paquete ejecuta lo que probé? | ZIP, configuración, arranque y verificación de App Service |
| 7. Entrega y operación | ¿Puedo recuperar y sostener lo prometido? | Restauración ensayada, expediente y acta para revisión |

Cada etapa contiene contexto, dos acciones sobre el proyecto, nombres sugeridos de entregables, todos sus temas ordenados y una autoevaluación. Las 78 lecciones participan en la navegación y en el progreso: no hay un subconjunto reducido ni temas plegados en una lista separada de ampliaciones. MSAL propio, Easy Auth, despliegue manual ZIP, CI/CD, dominios y otros escenarios se explican dentro de la etapa correspondiente, diferenciando su aplicabilidad.

## Taller de aceptación

`/ruta/vender/` presenta la primera reunión y doce familias de evaluación. Cada una relaciona la pregunta del cliente con requisito, evidencia, prueba, una respuesta insuficiente frecuente y las lecciones de implementación. El detalle de las 29 familias y el expediente/acta continúan en la lección 78.

La síntesis se contrastó con matrices de requisitos y declaraciones de cumplimiento, un anexo de obligaciones y soportes de identidad, segregación, respaldos, auditoría y arquitectura. Solo se incorporaron reformulaciones anónimas. Los documentos fuente, identificadores de empresas, personas, infraestructura y datos privados no se distribuyen en el repositorio.

Los parámetros de contraseñas, retención, notificación, disponibilidad y recuperación son perfiles contractuales de ejemplo. No son una política general impuesta por el curso ni una certificación. Cuando el mecanismo no demuestra lo exigido, la brecha continúa visible: MSAL no acredita todas las políticas de contraseña; ALLOWED_HOSTS no demuestra WAF; SCA no sustituye SAST/DAST; login no demuestra logout; un backup no demuestra restauración. Compartir servidor de base de datos mantiene dependencias de capacidad y administración aunque las bases se separen.

## Datos y navegación

- `academy/journey.json`: etapas, todos los temas, entregas y acciones.
- `academy/acceptance.json`: taller anónimo de requisitos y evidencias.
- `/`: portada de siete etapas.
- `/ruta/<slug>/`: trabajo de una etapa.
- `/biblioteca/`: catálogo y búsqueda; siguen funcionando los enlaces previos `/?q=` y `/?unit=`.
- `/tema/<id>/`: conserva la URL y el ID; la navegación anterior/siguiente incluye todas las lecciones de su etapa; al finalizar devuelve a la revisión de su entrega.
- `/historia/`: conserva escenas y cronología originales.
- El juego permanece en `/laboratorio/`; ya no ocupa la entrada del recorrido ni interrumpe la lección CQS.

El cuaderno existente conserva la clave `django-professional-course-v2`, sus notas y los IDs de los temas completados. La autoevaluación y la matriz usan otra clave: `django-professional-journey-v1`. El progreso de lectura se muestra por separado de la comprobación de entregables. No hay login ni escritura de catálogo.

La matriz permite guardar respuestas y descargar Markdown con su estado actual. No recibe secretos ni envía respuestas al servidor. La descarga sigue disponible si el almacenamiento local está bloqueado. Los botones de completado son autoevaluación; no validan controles del servicio ni conceden aprobación del cliente.

## Validación

```bash
python manage.py test academy
python manage.py check
```

Las pruebas cubren las 78 lecciones públicas, los siete recorridos, cobertura completa sin duplicados, navegación, biblioteca, anonimización, seguridad y reutilización de paginación. La revisión en navegador comprueba escritorio/móvil, matriz guardada y descargada, autoevaluación, preservación del cuaderno anterior y comportamiento al bloquear almacenamiento.

Esta reorganización no configura recursos en Azure, WAF, directorio, scanners ni workflows de revisión diaria. Esos controles se enseñan; sus evidencias deben obtenerse sobre cada proyecto y entorno que se entregue.
