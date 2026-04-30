from faker import Faker
import random
import csv

def generar_horarios_comercio():
    cantidad = random.randint(1, 2)
    horarios = []

    intentos = 0
    max_intentos = 50

    while len(horarios) < cantidad and intentos < max_intentos:
        intentos += 1

        inicio = random.randint(6, 20)  # 👈 más realista para comercios
        fin = random.randint(inicio + 2, 23)  # 👈 intervalos más amplios

        nuevo = (inicio, fin)

        # Validar no solapamiento
        solapa = False
        for (i, f) in horarios:
            if not (fin <= i or inicio >= f):
                solapa = True
                break
        
        if not solapa:
            horarios.append(nuevo)

    # Formato hora
    return [(f"{i:02d}:00:00", f"{f:02d}:00:00") for (i, f) in horarios]


def generar_comercios_csv(n, filename="backend/datos/csv/comercios.csv"):
    fake = Faker()

    categorias = [
        "ropa", "tecnologia", "supermercado", "restaurante",
        "farmacia", "banco", "entretenimiento"
    ]

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow([
            "id", "nombre", "categoria", "tipo",
            "horario_operacion", "riesgo"
        ])

        for i in range(1, n + 1):
            categoria = random.choice(categorias)
            tipo = random.choice(["fisico", "online"])

            # 🧠 Nombre coherente
            if categoria == "ropa":
                nombre = fake.company() + " Boutique"
            elif categoria == "tecnologia":
                nombre = fake.company() + " Tech"
            elif categoria == "supermercado":
                nombre = fake.company() + " Market"
            elif categoria == "restaurante":
                nombre = fake.company() + " Restaurant"
            elif categoria == "farmacia":
                nombre = fake.company() + " Farmacia"
            else:
                nombre = fake.company()

            # 🕒 Horarios
            if tipo == "online":
                # muchas tiendas online son 24/7
                if random.random() < 0.7:
                    horarios = [("00:00:00", "23:59:59")]
                else:
                    horarios = generar_horarios_comercio()
            else:
                horarios = generar_horarios_comercio()

           
            riesgo = False

            if tipo == "online" and random.random() < 0.3:
                riesgo = True
            
            if categoria == "tecnologia" and random.random() < 0.4:
                riesgo = True

            # aleatoriedad extra
            if random.random() < 0.1:
                riesgo = not riesgo

            writer.writerow([
                i,
                nombre,
                categoria,
                tipo,
                str(horarios),
                riesgo
            ])

    print(f"Archivo '{filename}' generado con {n} comercios.")

generar_comercios_csv(500)