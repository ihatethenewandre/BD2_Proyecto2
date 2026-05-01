from faker import Faker
import random
import csv
from datetime import datetime

def generar_relaciones_cuenta_transaccion(
    n_cuentas=1400,
    n_transacciones=2500,
    filename="backend/datos/csv/Rcuenta_transaccion.csv"
):
    fake = Faker()

    canales = ["app", "web", "cajero"]

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow([
            ":START_ID", ":END_ID",
            "fecha", "canal", "autenticado"
        ])

        for trans_id in range(1, n_transacciones + 1):
            #Distribución no uniforme (más realista)
            if random.random() < 0.7:
                cuenta_id = random.randint(1, int(n_cuentas * 0.3))  # cuentas más activas
            else:
                cuenta_id = random.randint(1, n_cuentas)

            # 📅 Fecha y hora completa
            fecha_datetime = fake.date_time_between(
                start_date='-2y',
                end_date='now'
            )

            canal = random.choice(canales)

          
            autenticado = True

            # cajero suele requerir autenticación
            if canal == "cajero":
                autenticado = True
            else:
                if random.random() < 0.1:  # 10% no autenticadas
                    autenticado = False

            writer.writerow([
                cuenta_id,
                trans_id,
                fecha_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                canal,
                autenticado
            ])

    print(f"Archivo '{filename}' generado con {n_transacciones} relaciones.")

generar_relaciones_cuenta_transaccion()