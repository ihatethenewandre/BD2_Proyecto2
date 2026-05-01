from faker import Faker
import random
import csv

def generar_relaciones_cliente_cuenta(
    n_clientes=1000,
    n_cuentas=1400,
    filename="backend/datos/csv/Rcliente_cuenta.csv"
):
    fake = Faker()

    relaciones = set()

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow([
            ":START_ID", ":END_ID",
            "fecha_apertura", "tipo_relacion", "activa"
        ])

        # 🔥 1. Relaciones 1 a 1 (primeros 1000)
        for i in range(1, n_clientes + 1):
            cliente_id = i
            cuenta_id = i

            relaciones.add((cliente_id, cuenta_id))

            writer.writerow([
                cliente_id,
                cuenta_id,
                fake.date_between(start_date='-10y', end_date='today'),
                "titular",
                random.random() > 0.05  # 95% activas
            ])

        # 🔥 2. Relaciones extra (400 restantes)
        cuenta_actual = n_clientes + 1

        while cuenta_actual <= n_cuentas:
            cliente_id = random.randint(1, n_clientes)
            cuenta_id = cuenta_actual

            if (cliente_id, cuenta_id) in relaciones:
                continue

            relaciones.add((cliente_id, cuenta_id))

            tipo = "titular" if random.random() < 0.85 else "cotitular"

            writer.writerow([
                cliente_id,
                cuenta_id,
                fake.date_between(start_date='-10y', end_date='today'),
                tipo,
                random.random() > 0.05
            ])

            cuenta_actual += 1

    print(f"Archivo '{filename}' generado con {n_cuentas} relaciones.")

generar_relaciones_cliente_cuenta()