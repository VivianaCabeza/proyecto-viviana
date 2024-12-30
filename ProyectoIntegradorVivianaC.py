import sqlite3
import os
from colorama import Fore, Style, init

# Inicializar colorama para colores en la terminal
init(autoreset=True)

# Conectar o crear la base de datos
conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()

# Crear tabla de productos 
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    numero_producto TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    categoria TEXT,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL
)              
''')

# Función para agregar un producto
def agregar_producto():
    numero_producto = input(Fore.LIGHTMAGENTA_EX + "Ingrese el número de producto:")
    
    # Verificar si el número del producto ya existe
    cursor.execute("SELECT * FROM productos WHERE numero_producto = ?",(numero_producto))
    if cursor.fetchone():
        print(Fore.RED + "Error: El número de producto ya existe.Intente con un número diferente.\n")
        return
    
    nombre = input(Fore.LIGHTMAGENTA_EX + "Ingrese el nombre del producto: ")
    descripción = input(Fore.LIGHTMAGENTA_EX + "Ingrese la descripción del producto: ")
    categoria = input(Fore.LIGHTMAGENTA_EX + "Ingrese la categoría del producto: ")
    try:
        cantidad = int(input(Fore.LIGHTMAGENTA_EX + "Ingrese la cantidad disponible: "))
        precio = float(input(Fore.LIGHTMAGENTA_EX + "Ingrese el precio del producto:"))
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a cero.")
    except ValueError as e:
        print(Fore.RED + f"Error: {e}\n")
        return    
    
    cursor.execute("INSERT INTO productos (numero_producto, nombre, descripcion, categoria, cantidad, precio) VALUES (?, ?, ?, ?, ?, ?)",
                (numero_producto, nombre, descripción, categoria, cantidad, precio))
    conn.commit()
    print(Fore.GREEN + f"Producto '{nombre}' agregado exitosamente.\n")

# Función para modificar un producto
def modificar_producto():
    numero_producto = input(Fore.LIGHTMAGENTA_EX + "Ingrese el número de producto que desea modificar: ")
    
    cursor.execute("SELECT * FROM productos WHERE numero_producto = ?",(numero_producto,))
    producto = cursor.fetchone()
    if not producto:
        print(Fore.RED + "Producto no encontrado.\n")
        return
    
    print(Fore.CYAN + f"Producto encontrado: Nombre: {producto[1]}, Descripción: {producto[2]}, Categoría: {producto[3]}, Cantidad: {producto[4]}, Precio:${producto[5]:.2f}")

    print(Fore.YELLOW + "1. Modificar nombre")
    print(Fore.YELLOW + "2. Modificar descripción")
    print(Fore.YELLOW + "3. Modificar categoría")
    print(Fore.YELLOW + "4. Modificar precio")
    print(Fore.YELLOW + "5. Modificar cantidad")
    opcion_modificar = input(Fore.LIGHTMAGENTA_EX + "Seleccione la opción de modificación (1-5): ")
    
    if opcion_modificar == '1':
        nuevo_nombre = input(Fore.LIGHTMAGENTA_EX + "Ingrese el nuevo nombre del producto: ")
        cursor.execute("UPDATE productos SET nombre = ? WHERE numero_producto = ?", (nuevo_nombre, numero_producto))
    elif opcion_modificar == '2':
        nueva_descripcion = input(Fore.LIGHTMAGENTA_EX + "Ingrese la nueva descripción del producto: ")
        cursor.execute("UPDATE productos SET descripcion = ? WHERE numero_producto = ?", (nueva_descripcion, numero_producto))
    elif opcion_modificar == '3':
        nueva_categoria = input(Fore.LIGHTMAGENTA_EX + "Ingrese la nueva categoría del producto: ")
        cursor.execute("UPDATE productos SET categoria = ? WHERE numero_producto = ?", (nueva_categoria, numero_producto))
    elif opcion_modificar == '4':
        nuevo_precio = float(input(Fore.LIGHTMAGENTA_EX + "Ingrese el nuevo precio del producto: "))
        cursor.execute("UPDATE productos SET precio = ? WHERE numero_producto = ?", (nuevo_precio, numero_producto))
    elif opcion_modificar == '5':
        nueva_cantidad = int(input(Fore.LIGHTMAGENTA_EX + "Ingrese la nueva cantidad del producto: "))
        cursor.execute("UPDATE productos SET cantidad = ? WHERE numero_producto = ?", (nueva_cantidad, numero_producto))
    else:
        print(Fore.RED + "Opción no válida.\n")
        return
    
    conn.commit()
    print(Fore.GREEN + "Producto modificado exitosamente.\n")

# Función para eliminar un producto
def eliminar_producto():
    numero_producto = input(Fore.LIGHTMAGENTA_EX + "Ingrese el número del producto que desea eliminar: ")
    
    cursor.execute("SELECT * FROM productos WHERE numero_producto = ?", (numero_producto,))
    producto = cursor.fetchone()
    if not producto:
        print(Fore.RED + "Producto no encontrado.\n")
        return
    
    cursor.execute("DELETE FROM productos WHERE numero_producto = ?", (numero_producto,))
    conn.commit()
    print(Fore.GREEN + f"Producto '{producto[1]}' eliminado exitosamente.\n")

# Función para mostrar inventario
def mostrar_inventario():
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    
    if not productos:
        print(Fore.YELLOW + "No hay productos en el inventario.\n")
        return
    
    print(Fore.BLUE + "\nInventario de productos:")
    print(Fore.CYAN + "{:<5} {:<20} {:<15} {:<20} {:<20} {:<10}".format("N°", "Nombre", "Descripción", "Categoría", "Cantidad", "Precio"))
    print(Fore.CYAN + "-" * 90)
    for i, producto in enumerate(productos, start=1):
        print(Fore.LIGHTBLUE_EX + "{:<5} {:<20} {:<15} {:<20} {:<10} ${:<10.2f}".format(i, producto[1], producto[2], producto[3], producto[4], producto[5]))
        if producto[4] < 5:
            print(Fore.RED + " ** Alerta: Bajo stock **")
    print("")

# Función para vender productos
def vender_producto():
    carrito = []
    while True:
        print(Fore.YELLOW + "\nProductos disponibles para la venta:")
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        
        for i, producto in enumerate(productos, start=1): 
            print(Fore.LIGHTBLUE_EX + f"{i}. Nombre: {producto[1]}, Cantidad: {producto[4]}, Precio: ${producto[5]:.2f}")
        
        try:
            indice = int(input(Fore.LIGHTMAGENTA_EX + "Ingrese el número del producto que desea agregar a la venta (0 para terminar): ")) - 1
            if indice == -1:
                break
            if 0 <= indice < len(productos):
                cantidad_vender = int(input(Fore.LIGHTMAGENTA_EX + "Ingrese la cantidad a vender: "))
                if 0 < cantidad_vender <= productos[indice][4]:
                    producto_seleccionado = {
                        'nombre': productos[indice][1],
                        'cantidad': cantidad_vender,
                        'precio_unitario': productos[indice][5],
                        'subtotal': cantidad_vender * productos[indice][5]
                    }
                    nuevo_stock = productos[indice][4] - cantidad_vender
                    cursor.execute("UPDATE productos SET cantidad = ? WHERE numero_producto = ?", (nuevo_stock, productos[indice][0]))
                    conn.commit()
                    carrito.append(producto_seleccionado)
                    print(Fore.GREEN + f"Producto '{producto_seleccionado['nombre']}' agregado al carrito.")
                else:    
                    print(Fore.RED + "Cantidad a vender no válida.\n")
            else:
                print(Fore.RED + "Número de producto no válido.\n")
        except ValueError:
            print(Fore.RED + "Error: La cantidad y número del producto deben ser válidos.\n")
    
    if carrito:
        print(Fore.BLUE + "\nCarrito de compras:")
        for i, item in enumerate(carrito, start=1):
            print(Fore.LIGHTBLUE_EX + f"{i}. {item['nombre']} - Cantidad: {item['cantidad']} - Subtotal: ${item['subtotal']:.2f}")
        total_venta = sum(item['subtotal'] for item in carrito)
        print(Fore.GREEN + f"Total a pagar: ${total_venta:.2f}")

# Menu principal 
while True:
    print(Fore.YELLOW + "Menú de gestión de inventario")
    print(Fore.LIGHTBLUE_EX + "1. Agregar producto")    
    print(Fore.LIGHTBLUE_EX + "2. Modificar producto")  
    print(Fore.LIGHTBLUE_EX + "3. Eliminar producto") 
    print(Fore.LIGHTBLUE_EX + "4. Mostrar inventario")
    print(Fore.LIGHTBLUE_EX + "5. Vender producto")  
    print(Fore.LIGHTBLUE_EX + "6. Salir")      
    opcion = input(Fore.LIGHTMAGENTA_EX + "Seleccione una opción (1-6):")
    
    if opcion == '1':
        agregar_producto()
    elif opcion == '2':
        modificar_producto()
    elif opcion == '3':
        eliminar_producto()
    elif opcion == '4':
        mostrar_inventario()
    elif opcion == '5':
        vender_producto()
    elif opcion == '6':
        print(Fore.GREEN + "Saliendo del programa...")
        break
    else:
        print(Fore.RED + "Opción no válida. Intente de nuevo.\n")
        
# Cerrar la conexión a la base de datos  al finalizar  
conn.close()