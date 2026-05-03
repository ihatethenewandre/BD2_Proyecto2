import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

class FraudModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        self.model_path = "fraud_model.pkl"

    def train_from_csv(self):
        try:
            # 1. Cargar CSVs
            df_trans     = pd.read_csv("datos/csv/transacciones.csv")
            df_clientes  = pd.read_csv("datos/csv/clientes.csv")
            df_comercios = pd.read_csv("datos/csv/comercios.csv")

            df_rel_cuenta_trans  = pd.read_csv("datos/csv/Rcuenta_transaccion.csv")
            df_rel_cliente_cuenta = pd.read_csv("datos/csv/Rcliente_cuenta.csv")
            df_rel_trans_comercio = pd.read_csv("datos/csv/Rtransaccion_comercio.csv")

            # 2. Renombrar columnas del formato Neo4j (:START_ID, :END_ID, id:ID)
            #    a nombres usables en pandas
            df_trans.rename(columns={"id:ID": "id_trans"}, inplace=True)
            df_clientes.rename(columns={"id:ID": "id_cliente"}, inplace=True)
            df_comercios.rename(columns={"id:ID": "id_comercio"}, inplace=True)

            # Rcuenta_transaccion: START=Cuenta → END=Transaccion
            df_rel_cuenta_trans.rename(
                columns={":START_ID": "id_cuenta", ":END_ID": "id_trans"}, inplace=True
            )
            # Rcliente_cuenta:  START=Cliente → END=Cuenta
            df_rel_cliente_cuenta.rename(
                columns={":START_ID": "id_cliente", ":END_ID": "id_cuenta"}, inplace=True
            )
            # Rtransaccion_comercio: START=Transaccion → END=Comercio
            df_rel_trans_comercio.rename(
                columns={":START_ID": "id_trans", ":END_ID": "id_comercio"}, inplace=True
            )

            # 3. Preparar slices limpios con columnas sin ambigüedad
            clientes_slim  = df_clientes[["id_cliente", "riesgo"]].rename(
                columns={"riesgo": "riesgo_cliente"}
            )
            comercios_slim = df_comercios[["id_comercio", "riesgo"]].rename(
                columns={"riesgo": "riesgo_comercio"}
            )

            # 4. MERGE: Transaccion → Cuenta → Cliente → riesgo_cliente
            paso1 = pd.merge(
                df_trans,
                df_rel_cuenta_trans[["id_trans", "id_cuenta"]],
                on="id_trans"
            )
            paso2 = pd.merge(
                paso1,
                df_rel_cliente_cuenta[["id_cuenta", "id_cliente"]],
                on="id_cuenta"
            )
            df_final = pd.merge(paso2, clientes_slim, on="id_cliente")

            # 5. MERGE: Transaccion → Comercio → riesgo_comercio
            df_final = pd.merge(
                df_final,
                df_rel_trans_comercio[["id_trans", "id_comercio"]],
                on="id_trans"
            )
            df_final = pd.merge(df_final, comercios_slim, on="id_comercio")

            # 6. Normalizar tipos
            #    riesgo_cliente ya es float (ej. 0.04)
            #    riesgo_comercio viene como string "True"/"False" desde el CSV
            df_final["riesgo_comercio"] = (
                df_final["riesgo_comercio"]
                .map({True: 1, False: 0, "True": 1, "False": 0})
                .fillna(0)
                .astype(int)
            )

            #    es_fraudulenta también puede venir como string
            df_final["es_fraudulenta"] = (
                df_final["es_fraudulenta"]
                .map({True: 1, False: 0, "True": 1, "False": 0})
                .fillna(0)
                .astype(int)
            )

            # 7. Features y etiqueta
            X = df_final[["monto", "riesgo_cliente", "riesgo_comercio"]]
            y = df_final["es_fraudulenta"]

            self.model.fit(X, y)
            joblib.dump(self.model, self.model_path)
            self.is_trained = True
            print(f"IA entrenada con {len(df_final)} transacciones reales de los CSV.")

        except Exception as e:
            import traceback
            print(f"Error al cruzar CSVs: {e}")
            traceback.print_exc()
            print("El modelo NO fue entrenado. Revisar los CSV y volver a iniciar.")

    def predict(self, monto: float, riesgo_cliente: float, riesgo_comercio: int):
        if not self.is_trained:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                self.is_trained = True
            else:
                return False

        prediction = self.model.predict([[monto, riesgo_cliente, riesgo_comercio]])
        return bool(prediction[0])

# Instancia global
fraud_ai = FraudModel()