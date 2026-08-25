# Restaurante App - Semana 11

## Mejoras Implementadas
- **Entidad Venta**: Creación de la clase `Venta` para relacionar `Usuario` y `Producto`.
- **Colecciones y Filtros**: Implementación del filtrado de operaciones por usuario en la capa de servicios.
- **Persistencia JSON**: Control de lectura/escritura de `productos.json`, `usuarios.json` y `ventas.json`.

## Estructura del Proyecto
- `datos/`: Archivos JSON de persistencia.
- `modelos/`: Clases `Producto`, `Usuario` y `Venta`.
- `servicios/`: `ArchivoServicio` y `Restaurante`.
- `main.py`: Interfaz por consola.

## Ejecución
```bash
python main.py