from faker import Faker
import random
import csv


def generar_relaciones_transaccion_destino(
    n_cuentas=1400,
    n_transacciones=2500,
    filename="backend/datos/csv/Rtransaccion_destino.csv"):
   

    fake = Faker()

    monedas = ["GTQ", "USD", "EUR"]

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow([
            ":START_ID", ":END_ID",
            "fecha", "tipo_transferencia", "moneda"
        ])

        for trans_id in range(1, n_transacciones + 1):

            tipo = "interna" if random.random() < 0.8 else "externa"

            # 🎯 destino SIEMPRE válido
            cuenta_destino = random.randint(1, n_cuentas)

            fecha = fake.date_time_between(
                start_date='-2y',
                end_date='now'
            )

            moneda = "GTQ" if tipo == "interna" else random.choice(monedas)

            writer.writerow([
                trans_id,
                cuenta_destino,
                fecha.strftime("%Y-%m-%d %H:%M:%S"),
                tipo,
                moneda
            ])

    print(f"Archivo '{filename}' generado correctamente sin IDs inválidos.")

generar_relaciones_transaccion_destino()