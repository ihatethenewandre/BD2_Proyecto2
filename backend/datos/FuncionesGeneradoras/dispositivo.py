from faker import Faker
import random
import csv

def generar_dispositivos_csv(n, filename="backend/datos/csv/dispositivos.csv"):
    fake = Faker('es_ES')
    
    tipos = ["telefono", "computadora", "tablet"]
    
    sistemas_por_tipo = {
        "telefono": ["Android", "iOS"],
        "computadora": ["Windows", "Linux", "macOS"],
        "tablet": ["Android", "iOS"]
    }
    
    # Rangos de precio por tipo (USD aprox)
    precios = {
        "telefono": (50, 1500),
        "computadora": (300, 3000),
        "tablet": (100, 1200)
    }

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        writer.writerow([
            "id", "tipo", "ip", "sistema_operativo", "confiable", "precio"
        ])
        
        for i in range(1, n + 1):
            tipo = random.choice(tipos)
            sistema = random.choice(sistemas_por_tipo[tipo])
            ip = fake.ipv4()
            
            # Precio según tipo
            precio_min, precio_max = precios[tipo]
            precio = round(random.uniform(precio_min, precio_max), 2)
            
            # Lógica de confiabilidad
            confiable = True
            
            # Dispositivos muy baratos → sospechosos
            if precio < (precio_min + (precio_max - precio_min) * 0.2):
                if random.random() < 0.6:
                    confiable = False
            
            # IPs privadas pueden ser más confiables (opcional)
            if ip.startswith("192.168") or ip.startswith("10."):
                if random.random() < 0.7:
                    confiable = True
            
            # Un poco de aleatoriedad
            if random.random() < 0.1:
                confiable = not confiable
            
            writer.writerow([
                i,
                tipo,
                ip,
                sistema,
                confiable,
                precio
            ])

    print(f"Archivo '{filename}' generado con {n} dispositivos.")

generar_dispositivos_csv(2000)