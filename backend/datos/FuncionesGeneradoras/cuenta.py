from faker import Faker
import random
import csv

def generar_horarios():
    cantidad = random.randint(1, 3)
    horarios = []

    intentos = 0
    max_intentos = 50 

    while len(horarios) < cantidad and intentos < max_intentos:
        intentos += 1

        inicio = random.randint(0, 22)
        fin = random.randint(inicio + 1, 23)
        nuevo = (inicio, fin)

        # Validar que no haya solapamiento
        solapa = False
        for (i, f) in horarios:
            if not (fin <= i or inicio >= f):
                solapa = True
                break
        
        if not solapa:
            horarios.append(nuevo)

   
    
    horarios_formateados = [
        (f"{i:02d}:00:00", f"{f:02d}:00:00")
        for (i, f) in horarios
    ]

    return horarios_formateados

def generar_cuentas_csv(n, filename="backend/datos/csv/cuentas.csv"):
    fake = Faker()
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Encabezados
        writer.writerow([
            "id", "saldo", "fecha_creacion", "estado",
            "promedio_uso", "horario_promedio_uso"
        ])
        
        for i in range(1, n + 1):
            saldo = round(random.uniform(0, 50000), 2)
            fecha_creacion = fake.date_between(start_date='-10y', end_date='today')
            estado = random.choice([True, False])
            promedio_uso = round(random.uniform(50, 5000), 2)
            horarios = generar_horarios()
            
            writer.writerow([
                i,
                saldo,
                fecha_creacion,
                estado,
                promedio_uso,
                str(horarios)  
            ])
            print(i)

    print(f"Archivo '{filename}' generado con {n} cuentas.")

generar_cuentas_csv(1400)