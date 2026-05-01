from faker import Faker
import random
import csv

def cargar_ips_dispositivos(filename="backend/datos/csv/dispositivos.csv"):
    ips = {}

    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ips[int(row["id:ID"])] = row["ip"]

    return ips


def generar_relaciones_transaccion_dispositivo(
    n_transacciones=2500,
    n_dispositivos=2000,
    dispositivos_file="backend/datos/csv/dispositivos.csv",
    filename="backend/datos/csv/Rtransaccion_dispositivo.csv"
):
    fake = Faker()

    # 🔥 cargar IPs reales
    ips_dispositivos = cargar_ips_dispositivos(dispositivos_file)

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow([
            ":START_ID", ":END_ID",
            "fecha", "ip", "autenticacion_fuerte"
        ])

        for trans_id in range(1, n_transacciones + 1):

            # 🧠 dispositivos más usados
            if random.random() < 0.7:
                dispositivo_id = random.randint(1, int(n_dispositivos * 0.3))
            else:
                dispositivo_id = random.randint(1, n_dispositivos)

            # 📅 fecha
            fecha = fake.date_time_between(
                start_date='-2y',
                end_date='now'
            )

            # 🌐 IP del dispositivo
            ip = ips_dispositivos.get(dispositivo_id, fake.ipv4())

            # 🔐 autenticación fuerte
            autenticacion_fuerte = True

            # algunos casos sin autenticación fuerte
            if random.random() < 0.15:
                autenticacion_fuerte = False

            writer.writerow([
                trans_id,
                dispositivo_id,
                fecha.strftime("%Y-%m-%d %H:%M:%S"),
                ip,
                autenticacion_fuerte
            ])

    print(f"Archivo '{filename}' generado con {n_transacciones} relaciones.")

generar_relaciones_transaccion_dispositivo()