from faker import Faker
import random
import csv
from datetime import datetime, timedelta

def generar_transacciones_csv(n, filename="backend/datos/csv/transacciones.csv"):
    fake = Faker()
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Encabezados
        writer.writerow(["id", "monto", "fecha", "hora", "es_fraudulenta"])
        
        for i in range(1, n + 1):
            # Generar fecha reciente
            fecha = fake.date_between(start_date='-2y', end_date='today')
            
            # Generar hora
            hora_dt = fake.time_object()
            hora = hora_dt.strftime("%H:%M:%S")
            
            # Monto normal
            monto = round(random.uniform(10, 5000), 2)
            
            # Lógica de fraude
            es_fraudulenta = False
            
            # 1. Probabilidad base baja
            if random.random() < 0.05:
                es_fraudulenta = True
            
            # 2. Montos muy altos → sospechoso
            if monto > 4000 and random.random() < 0.5:
                es_fraudulenta = True
            
            # 3. Horarios nocturnos → más riesgo
            hora_int = hora_dt.hour
            if (hora_int < 5 or hora_int > 23) and random.random() < 0.3:
                es_fraudulenta = True
            
            # 4. Si es fraude, a veces exageramos el monto 
            if es_fraudulenta and random.random() < 0.5:
                monto = round(random.uniform(5000, 20000), 2)
            
            writer.writerow([
                i,
                monto,
                fecha,
                hora,
                es_fraudulenta
            ])

    print(f"Archivo '{filename}' generado con {n} transacciones.")

generar_transacciones_csv(2500)