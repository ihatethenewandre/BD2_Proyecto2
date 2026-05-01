from faker import Faker
import random
import csv

def generar_relaciones_cuenta_dispositivo(
    n_cuentas=1400,
    n_dispositivos=2000,
    filename="backend/datos/csv/Rcuenta_dispositivo.csv"
):
    fake = Faker()

    relaciones = set()

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow([
            ":START_ID", ":END_ID",
            "fecha_vinculacion", "tipo_acceso", "activo"
        ])

        for cuenta_id in range(1, n_cuentas + 1):

            # 👇 cada cuenta tiene al menos 1 dispositivo
            cantidad = 1

            # algunas tienen más
            if random.random() < 0.6:
                cantidad += random.randint(1, 2)

            for _ in range(cantidad):

                # evitar duplicados
                while True:
                    dispositivo_id = random.randint(1, n_dispositivos)
                    if (cuenta_id, dispositivo_id) not in relaciones:
                        relaciones.add((cuenta_id, dispositivo_id))
                        break

                # 📅 fecha
                fecha = fake.date_between(
                    start_date='-3y',
                    end_date='today'
                )

                # 🔐 tipo de acceso
                tipo_acceso = "login" if random.random() < 0.7 else "token"

                # 🧠 activo
                activo = True

                # dispositivos antiguos o poco usados → más chance de inactivo
                if random.random() < 0.1:
                    activo = False

                writer.writerow([
                    cuenta_id,
                    dispositivo_id,
                    fecha,
                    tipo_acceso,
                    activo
                ])

    print(f"Archivo '{filename}' generado correctamente.")

generar_relaciones_cuenta_dispositivo()