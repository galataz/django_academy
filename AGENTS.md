# Convenciones de este proyecto educativo

- Mantener la academia pública, sin añadir login ni CRUD de escritura sobre el catálogo.
- Antes de crear una Query de API, leer `repoGenerico/views_base.py` y
  `academy/views/queries/catalog.py`. Reutilizar la base y sus hooks.
- No duplicar paginación, Paginator, validación de parámetros o envolturas JSON
  en las vistas consumidoras. Proponer cambios comunes en repoGenerico.
- Conservar el contrato descrito en `repoGenerico/CONTRACT.md` y probar cambios
  contra al menos dos consumidores si afectan el flujo compartido.
- No asumir que un hook de DRF existe en una clase propia: comprobar que se llama.
- El contenido enseña una biblioteca más amplia que la implementada en esta
  academia. Distinguir código ejecutable, ejemplos didácticos y mejoras propuestas.
- Conservar IDs de lecciones, progreso y notas. Leer/escribir JSON como UTF-8.
