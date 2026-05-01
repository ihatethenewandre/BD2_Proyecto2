from faker import Faker
import random
import csv

def generar_relaciones_transaccion_comercio(
    n_transacciones=2500,
    n_comercios=500,
    filename="backend/datos/csv/Rtransaccion_comercio.csv"
):
    fake = Faker()

    metodos = ["tarjeta", "QR", "NFC"]

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow([
            ":START_ID", ":END_ID",
            "fecha", "metodo_pago", "presencial"
        ])

        for trans_id in range(1, n_transacciones + 1):

            # 🧠 Comercios populares (más tráfico)
            if random.random() < 0.7:
                comercio_id = random.randint(1, int(n_comercios * 0.3))
            else:
                comercio_id = random.randint(1, n_comercios)

            # 📅 Fecha
            fecha = fake.date_time_between(
                start_date='-2y',
                end_date='now'
            )

            metodo = random.choice(metodos)

            # 🧠 Presencial (lógica probabilística)
            if metodo == "NFC":
                presencial = True
            elif metodo == "QR":
                presencial = random.random() < 0.6
            else:  # tarjeta
                presencial = random.random() < 0.7

            writer.writerow([
                trans_id,
                comercio_id,
                fecha.strftime("%Y-%m-%d %H:%M:%S"),
                metodo,
                presencial
            ])

    print(f"Archivo '{filename}' generado con {n_transacciones} relaciones.")

generar_relaciones_transaccion_comercio()