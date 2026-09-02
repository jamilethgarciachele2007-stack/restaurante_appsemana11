# Restaurante App - Optimización de Colecciones (Semana 12)

Proyecto correspondiente a la **Semana 12** de Programación Orientada a Objetos, enfocado en la mejora de rendimiento mediante el uso de colecciones optimizadas en memoria.

## Arquitectura y Optimizaciones Aplicadas

Se conservaron las colecciones principales en forma de listas (`list`) dentro de `servicios/restaurante.py` para la persistencia en formato JSON y los recorridos generales, incorporando las siguientes **estructuras auxiliares**:

* **`_productos_por_codigo` (`dict`):** Permite la búsqueda directa $O(1)$ de productos a partir de su código único.
* **`_usuarios_por_identificacion` (`dict`):** Permite la localización $O(1)$ de usuarios mediante su número de cédula/identificación.
* **`_ventas_por_usuario` (`dict`):** Mantiene agrupadas las ventas por cada usuario, evitando filtrados iterativos sobre la totalidad de las ventas registradas.

## Sincronización y Persistencia

1. **Carga e Inicialización:** Al arrancar el sistema, el método `_reconstruir_indices()` lee las listas deserializadas de `datos/*.json` e inicializa automáticamente los diccionarios auxiliares.
2. **Coherencia de Datos:** Cada alta de información (usuario, producto o venta) actualiza simultáneamente la lista principal, la estructura auxiliar correspondiente y el archivo de persistencia JSON.