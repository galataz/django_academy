# Expediente de aceptación industrial — SensorHub

Modelo didáctico. Completar y revisar con las áreas responsables. No es una
certificación, un acta firmada ni una aprobación de salida.

## 1. Ficha de entrega

- Servicio y versión/commit: [completar]
- Objetivo, procesos y criticidad: [completar]
- Alcance contratado y exclusiones: [completar]
- Ambientes, región y modelo de servicio: [completar]
- Responsable del proveedor y responsables del cliente por función: [completar]
- Documentos de requisitos vigentes y precedencia acordada: [completar]

## 2. Índice de evidencias

1. Arquitectura, componentes y límites de confianza.
2. Inventario de integraciones, protocolos, autenticación, volumen y reintentos.
3. Identidad, MFA, roles, altas, bajas y cuentas técnicas.
4. Entornos, datos de prueba, aislamiento y acceso de administración.
5. Settings efectivos, perímetro, WAF y línea base de endurecimiento.
6. Inventario de datos, cifrado, claves y retención.
7. Auditoría, vigilancia y recepción de eventos de seguridad.
8. Desarrollo seguro, versiones, informes y remediación comprobada.
9. Respaldo, restauración ensayada, RTO, RPO y disponibilidad.
10. Incidentes, cambios, reversión, soporte y fin del servicio.
11. Equipos y personal del proveedor.
12. Matriz, decisiones y acta de compromiso.

Para cada evidencia: ID, control relacionado, versión, entorno, fecha, autor,
procedimiento, resultado, limitaciones y ubicación privada autorizada.

## 3. Matriz por control

| ID | Requisito y fuente vigente | Obligatorio / bloqueante | Alcance | Responsable | Estado | Evidencia y prueba | Brecha | Decisión |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SEC-AUD-02 | Registrar cierre explícito de sesión | Sí / por acordar | Web / QA | Desarrollo | Pendiente de evidencia | Por ejecutar | Login disponible; logout sin verificar | Pendiente |
| SEC-NET-01 | WAF efectivo para el ingreso web | Según contrato | Producción | Infraestructura | Pendiente | Política y evento de bloqueo | Hosts no acreditan WAF | Pendiente |

Estados: Cumple verificado, Parcial, Pendiente de evidencia, No cumple,
No aplica propuesto, Excepción aceptada. La excepción conserva su riesgo,
aprobador, controles compensatorios y expiración; no demuestra cumplimiento
del mecanismo originalmente pedido.

## 4. Registro de prueba de recuperación

- Escenario, autorización y participantes: [completar]
- Componentes, versión y punto de recuperación: [completar]
- Objetivos RTO/RPO aprobados y alcance de medición: [completar]
- Inicio del incidente simulado, detección e inicio de recuperación: [completar]
- Fin de restauración y fin de validación funcional/seguridad: [completar]
- Último dato esperado y último dato recuperado: [completar]
- Tiempo de recuperación y pérdida temporal medidos: [completar]
- Integridad, permisos, autenticación, cifrado e ingesta: [completar]
- Hallazgos, responsables, correcciones y repetición: [completar]
- Resultado y revisión: [completar]

## 5. Acta de compromiso y revisión técnica — borrador

### Identificación

Servicio, versión, fecha, alcance, ambientes y participantes autorizados:
[completar]. Adjuntar matriz versionada e índice de evidencias.

### Controles verificados

Relacionar IDs, evidencia, prueba, resultado y revisor. No marcar como verificado
un control pendiente, una intención ni una recomendación.

### Brechas y compromisos

| ID | Brecha | Acción | Responsable | Fecha acordada | Prueba de cierre | Bloqueante |
| --- | --- | --- | --- | --- | --- | --- |
| [ID] | [describir] | [implementar / probar] | [función] | [fecha] | [resultado esperado] | [sí/no] |

### Excepciones

Para cada excepción: requisito original, motivo, riesgo, alcance, control
compensatorio, responsable, aprobador autorizado, vigencia y revisión.
Un No aplica propuesto necesita la decisión del revisor.

### Operación y obligaciones

- Soporte, cobertura y escalamiento: [completar]
- Incidentes: plazos, evento que inicia el reloj y canal privado: [completar]
- RTO/RPO, retención y evidencia de ensayo: [completar]
- Disponibilidad: ventana, alcance, medición y exclusiones: [completar]
- Parcheo, cambios, reversión y nueva evidencia: [completar]
- Datos: uso, propiedad, devolución, borrado y copias retenidas: [completar]
- Licencia, código y límites de mantenimiento: [completar]
- Cambios de exigencia y revisión de compromisos: [completar]

### Decisión de salida

Decisión: [pendiente / aprobada / condicionada / rechazada].
Condiciones, alcance, autoridad competente y fecha: [completar].
Los bloqueantes abiertos requieren corrección o una decisión excepcional
expresa de la autoridad competente. Esta plantilla no autoriza la salida.

### Aprobaciones

Responsables por función y mecanismo de aprobación: [completar].
Conservar la aprobación vinculada a una versión concreta del expediente.

## 6. Versión pública del aprendizaje

Publicar solo un material reconstruido con datos sintéticos. No incluir
formularios de cliente, firmas, contactos, marcas, códigos internos, dominios,
direcciones, usuarios, tenant IDs, credenciales ni capturas reales.
