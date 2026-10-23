# Contrato de la base pública

La biblioteca compartida del equipo se enseña en los temas 9 y 10. Este proyecto
implementa un subconjunto: `BaseListQueryView` para el catálogo público.

## Entrada

- `page`: entero >= 1, por defecto 1.
- `per_page`: entero entre 1 y 100, por defecto 10.
- `ordering`: campo autorizado, opcionalmente con `-`; por defecto `number`.
- `search`: máximo 200 caracteres en esta implementación.

Entradas de página/tamaño inválidas u orden no autorizado producen 400 con
`success: false` y `error`. `Paginator.get_page` normaliza páginas que exceden
el rango disponible. Un resultado vacío conserva la representación del paginador.

## Salida

`success`, `results`, `total_count`, `current_page`, `total_pages`.

`total_count` cuenta después de la búsqueda sobre `get_queryset()`. Para una
aplicación privada, ese queryset debe estar previamente restringido al alcance
permitido. Esta academia contiene únicamente información pública.

## Extensión

Declarar `model`, `serializer_class` y `allowed_ordering`; sobreescribir
`get_queryset()` y `apply_search(queryset, search)` cuando corresponda.
El handler `get` y `Paginator` permanecen en la base. Cambiar el campo de orden
predeterminado requiere ampliar la base: no basta con cambiar allowed_ordering.

La familia completa enseñada tiene otros nombres de hooks y contratos:
`BaseListView` usa `apply_search_filters` y puede adaptar DataTables.
No importar esas clases como si ya existieran en este subconjunto.

## Revisión humana y con IA

Leer una Query existente antes de generar otra. No introducir otra forma de
paginar, claves JSON distintas o límites nuevos sin documentar la decisión.
Para extender, comprobar entradas inválidas, búsqueda, conjunto vacío, conteo,
orden y dos subclases consumidoras. No reducir líneas quitando permisos.
