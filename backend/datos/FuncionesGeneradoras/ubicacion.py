
from faker import Faker
import random
import csv

from faker import Faker
import random
import csv

def generar_ubicaciones_csv(n, filename="backend/datos/csv/ubicaciones.csv"):
    fake = Faker('es_ES')
    
    continentes = [
        "América", "Europa", "Asia", "África", "Oceanía"
    ]
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        writer.writerow([
            "id", "continente", "pais", "ciudad",
            "latitud", "longitud", "zona_riesgo"
        ])
        
        for i in range(1, n + 1):  # 👈 FIX
            pais = fake.country()
            ciudad = fake.city()
            latitud = float(fake.latitude())
            longitud = float(fake.longitude())
            continente = random.choice(continentes)
            
            # 🧠 Lógica de riesgo
            zona_riesgo = False
            
            if continente in ["África", "América"] and random.random() < 0.3:
                zona_riesgo = True
            
            if abs(latitud) > 60 and random.random() < 0.4:
                zona_riesgo = True
            
            writer.writerow([
                i,  # 👈 ID único
                continente,
                pais,
                ciudad,
                latitud,
                longitud,
                zona_riesgo
            ])

    print(f"Archivo '{filename}' generado con {n} ubicaciones.")

generar_ubicaciones_csv(800)