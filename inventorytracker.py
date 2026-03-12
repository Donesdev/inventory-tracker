import csv
from datetime import datetime

def get_number(promt):
    while True:
        s = input(promt).strip()

        # keep digits, minus sign, and decimal point
        cleaned = ''.join(ch for ch in s if ch.isdigit() or ch in '.-')
        
        # Handle empty / invalid cases
        if cleaned in ("", "-", ".", "-."):
            print("Por favor escribe un numero (e.j: 12, 12.50, $12).")
            continue
        try:
            return float(cleaned)
        except ValueError:
            print("Numero invalido. Intenta otra vez.")

def menu():
    print('''
          1. Agregar compra
          2. Agregar Venta
          3. Ver Resumen
          4. Salir
          ''')
    while True:
        eleccion = input("Elige un numero: ").strip()
        if eleccion.isdigit() and 1 <= int(eleccion) <= 4:
            return int(eleccion)
        print("Opcion invalida. Elige 1, 2, 3, o 4")

def guardar_compra(fecha, producto, costo, shipping, total):
    # Si el archivo no exitste, crea el header primero
    try:
        with open("compras.csv", "r", newline="", encoding="utf-8"):
            existe = True
    except FileNotFoundError:
        existe = False

        with open("compras.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not existe:
                writer.writerow(["fecha", "producto", "costo", "shipping", "total"])
            writer.writerow([fecha, producto, f"{costo:.2f}", f"{shipping:.2f}", f"{total:.2f}"])
def agregar_compra():
    producto = input("Que producto compraste?: ").strip()
    costo = get_number("Cuanto pagaste por el producto?: ")
    shipping = get_number("Cuanto pagaste por el shipping/evio?: ")
    total = costo + shipping
    fecha = datetime.now().strftime("%Y-%m-%d")

    guardar_compra(fecha, producto, costo, shipping, total)

    print(f"\n✅ Compra de guardada: {producto}")
    print(f" Costo: ${costo:.2f}")
    print(f" Shipping: ${shipping:.2f}")
    print(f" Total: ${total:.2f}")

def ver_resumen():
    print("Mostrando resumen...")
    try:
        with open("compras.csv", "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            total_invertido = 0
            cantidad_productos = 0

            for row in reader:
                total_invertido += float(row["total"])
                cantidad_productos += 1
        print("\n📊 RESUMEN")
        print(f"Productos comprados: {cantidad_productos}")
        print(f"Total invertiodo: ${total_invertido:.2f}\n")

    except FileNotFoundError:
        print("No hay compras registradas todavia.\n")

def main():
    while True:
        eleccion = menu()
        if eleccion == 1:
            agregar_compra()
        elif eleccion == 2:
            print("Todavia no hicimos agregar_venta")
        elif eleccion == 3:
            ver_resumen()
        else:
            print("Saliendo...")
            break
main()