from faker import Faker
import random
import csv

def generar_relaciones_comercio_ubicacion(
    n_comercios=500,
    n_ubicaciones=800,
    filename="backend/datos/csv/Rcomercio_ubicacion.csv"
):
    fake = Faker()

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow([
            ":START_ID", ":END_ID",
            "fecha_registro", "tipo_zona", "zona_riesgo"
        ])

        for comercio_id in range(1, n_comercios + 1):

            # 📍 asignar ubicación
            ubicacion_id = random.randint(1, n_ubicaciones)

            # 📅 fecha
            fecha = fake.date_between(
                start_date='-10y',
                end_date='today'
            )

            # 🧠 tipo de zona
            if random.random() < 0.7:
                tipo_zona = "urbana"
            else:
                tipo_zona = "rural"

            # 🚨 zona de riesgo
            zona_riesgo = False

            if tipo_zona == "rural" and random.random() < 0.4:
                zona_riesgo = True

            # pequeña aleatoriedad
            if random.random() < 0.1:
                zona_riesgo = not zona_riesgo

            writer.writerow([
                comercio_id,
                ubicacion_id,
                fecha,
                tipo_zona,
                zona_riesgo
            ])

    print(f"Archivo '{filename}' generado correctamente.")

generar_relaciones_comercio_ubicacion()