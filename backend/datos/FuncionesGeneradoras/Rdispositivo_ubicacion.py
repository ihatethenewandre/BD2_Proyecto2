from faker import Faker
import random
import csv

def generar_relaciones_dispositivo_ubicacion(
    n_dispositivos=2000,
    n_ubicaciones=800,
    filename="backend/datos/csv/Rdispositivo_ubicacion.csv"
):
    fake = Faker()

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow([
            ":START_ID", ":END_ID",
            "fecha_registro", "precision", "fuente"
        ])

        for dispositivo_id in range(1, n_dispositivos + 1):

            # 📍 asignar ubicación (puede repetirse, está bien)
            ubicacion_id = random.randint(1, n_ubicaciones)

            # 📅 fecha
            fecha = fake.date_between(
                start_date='-3y',
                end_date='today'
            )

            # 📡 fuente
            if random.random() < 0.7:
                fuente = "GPS"
                precision = round(random.uniform(5, 30), 2)
            else:
                fuente = "IP"
                precision = round(random.uniform(50, 5000), 2)

            writer.writerow([
                dispositivo_id,
                ubicacion_id,
                fecha,
                precision,
                fuente
            ])

    print(f"Archivo '{filename}' generado con {n_dispositivos} relaciones.")

generar_relaciones_dispositivo_ubicacion()