from faker import Faker
import random
import csv
from datetime import timedelta

def generar_relaciones_cliente_ubicacion(
    n_clientes=1000,
    n_ubicaciones=800,
    filename="backend/datos/csv/Rcliente_ubicacion.csv"
):
    fake = Faker()

    relaciones = []

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow([
            ":START_ID", ":END_ID",
            "fecha_inicio", "fecha_fin", "vacaciones"
        ])

        for cliente_id in range(1, n_clientes + 1):

            # 🏠 residencia principal
            ubicacion_id = random.randint(1, n_ubicaciones)

            fecha_inicio = fake.date_between(start_date='-10y', end_date='-1y')

            writer.writerow([
                cliente_id,
                ubicacion_id,
                fecha_inicio,
                "",  # 👈 null para Neo4j
                False
            ])

            # 🌍 posibilidad de otra relación (mudanza o vacaciones)
            if random.random() < 0.4:

                ubicacion_id2 = random.randint(1, n_ubicaciones)

                # evitar misma ubicación
                while ubicacion_id2 == ubicacion_id:
                    ubicacion_id2 = random.randint(1, n_ubicaciones)

                vacaciones = random.random() < 0.5

                if vacaciones:
                    # 🏖️ vacaciones (corto)
                    inicio = fake.date_between(start_date='-2y', end_date='today')
                    duracion = random.randint(3, 30)
                    fin = inicio + timedelta(days=duracion)
                else:
                    # 🏠 segunda residencia o mudanza
                    inicio = fake.date_between(start_date='-5y', end_date='-1y')

                    # 50% sigue vigente
                    if random.random() < 0.5:
                        fin = ""
                    else:
                        duracion = random.randint(180, 1500)
                        fin = inicio + timedelta(days=duracion)

                writer.writerow([
                    cliente_id,
                    ubicacion_id2,
                    inicio,
                    fin,
                    vacaciones
                ])

    print(f"Archivo '{filename}' generado correctamente.")

generar_relaciones_cliente_ubicacion()