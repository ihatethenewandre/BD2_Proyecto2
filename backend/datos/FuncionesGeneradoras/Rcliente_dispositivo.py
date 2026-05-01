from faker import Faker
import random
import csv
from faker import Faker
import random
import csv

def cargar_confiabilidad_dispositivos(filename="backend/datos/csv/dispositivos.csv"):
    confiables = {}

    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            confiables[int(row["id:ID"])] = row["confiable"].strip().lower() == "true"

    return confiables


def generar_relaciones_cliente_dispositivo(
    n_clientes=1000,
    n_dispositivos=2000,
    dispositivos_file="backend/datos/csv/dispositivos.csv",
    filename="backend/datos/csv/Rcliente_dispositivo.csv"
):
    fake = Faker()

    confiabilidad_disp = cargar_confiabilidad_dispositivos(dispositivos_file)

    relaciones = set()

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow([
            ":START_ID", ":END_ID",
            "fecha_ultimo_uso", "frecuencia", "confiable"
        ])

        for cliente_id in range(1, n_clientes + 1):

            # 👇 cada cliente tiene al menos 1 dispositivo
            cantidad = 1

            # algunos tienen más
            if random.random() < 0.5:
                cantidad += random.randint(1, 3)

            for _ in range(cantidad):

                # evitar duplicados
                while True:
                    dispositivo_id = random.randint(1, n_dispositivos)
                    if (cliente_id, dispositivo_id) not in relaciones:
                        relaciones.add((cliente_id, dispositivo_id))
                        break

                # 📅 fecha
                fecha = fake.date_time_between(
                    start_date='-2y',
                    end_date='now'
                )

                # 🔢 frecuencia
                frecuencia = random.randint(1, 500)

                # 🧠 confiabilidad
                confiable = True

                # si el dispositivo no es confiable → más probable falso
                if not confiabilidad_disp.get(dispositivo_id, True):
                    if random.random() < 0.6:
                        confiable = False

                # si lo usa poco → sospechoso
                if frecuencia < 5 and random.random() < 0.5:
                    confiable = False

                # pequeña aleatoriedad
                if random.random() < 0.1:
                    confiable = not confiable

                writer.writerow([
                    cliente_id,
                    dispositivo_id,
                    fecha.strftime("%Y-%m-%d %H:%M:%S"),
                    frecuencia,
                    confiable
                ])

    print(f"Archivo '{filename}' generado correctamente.")

generar_relaciones_cliente_dispositivo()