from faker import Faker
import random
import csv

def generar_clientes_csv(n, filename="backend/datos/csv/clientes.csv"):
    fake = Faker('es_ES')
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Encabezados
        writer.writerow(["id", "nombre", "fecha_nacimiento", "riesgo", "sueldo", "empleo"])
        
        for i in range(1, n + 1):
            nombre = fake.name()
            fecha_nacimiento = fake.date_of_birth(minimum_age=18, maximum_age=80)
            riesgo = round(random.uniform(0, 1), 2)
            sueldo = round(random.uniform(3000, 20000), 2)
            empleo = fake.job()
            
            writer.writerow([i, nombre, fecha_nacimiento, riesgo, sueldo, empleo])

    print(f"Archivo '{filename}' generado con {n} clientes.")


generar_clientes_csv(1000)