from servicios.restaurante import Restaurante

def mostrar_menu():
    print("\n--- SISTEMA RESTAURANTE_APP (SEMANA 11) ---")
    print("1. Registrar venta")
    print("2. Consultar ventas por usuario")
    print("3. Salir")

def ejecutar():
    restaurante = Restaurante()
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            usr_id = input("Ingrese identificación del usuario: ")
            prod_cod = input("Ingrese código del producto: ")
            try:
                cant = int(input("Ingrese cantidad a comprar: "))
                exito = restaurante.vender_producto(prod_cod, usr_id, cant)
                if exito:
                    print("¡Venta registrada y stock actualizado con éxito!")
                else:
                    print(" Error: Usuario/Producto no encontrado o stock insuficiente.")
            except ValueError:
                print(" Error: Debe ingresar una cantidad numérica válida.")

        elif opcion == "2":
            usr_id = input("Ingrese identificación del usuario a consultar: ")
            ventas = restaurante.consultar_ventas_usuario(usr_id)
            if not ventas:
                print("No se encontraron ventas para este usuario.")
            else:
                print(f"\n--- Ventas del Usuario {usr_id} ---")
                for v in ventas:
                    prod = restaurante.buscar_producto(v.producto_codigo)
                    nombre_p = prod.nombre if prod else "Producto desconocido"
                    print(f"- Producto: {nombre_p} (Código: {v.producto_codigo}) | Cantidad: {v.cantidad}")

        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    ejecutar()