
# Extraer datos del Correo

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from O365 import Account

# Esto busca el archivo .env un nivel arriba de donde está el script
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


def conectar_graph_api():
    """Funcion para autenticarse con la API de Microsoft."""
    # Pegamos aqui las llaves (IDs y el secreto value cree)
    CLIENT_ID = os.getenv('CLIENT_ID')
    SECRET_VALUE = os.getenv('SECRET_VALUE')

    if not CLIENT_ID or not SECRET_VALUE:
        raise ValueError("Las variables de entorno CLIENT_ID o SECRET_VALUE no estan definidas")

    credentials = (CLIENT_ID, SECRET_VALUE)
    account = Account(credentials)

    #Logica de autenticacion con la url local
    if not account.is_authenticated:
        print("Iniciando autenticacion por primera vez...")
        # Definimos la url que pusimos en Azure
        # url_nativa = 'https://login.microsoftonline.com/common/oauth2/nativeclient'
        url_choque = 'http://localhost:8080'
        # Iniciamos la autenticacion indicando que queremos que se quede en consola
        # Esto evita que el proceso expire tan rapido
        # account.authenticate(scopes=['basic','message_all'], redirect_uri=url_nativa)
        account.authenticate(scopes=['https://graph.microsoft.com/Mail.Read'],redirect_uri=url_choque)
    ### este else me da mala espina, estar pendiente.
    else:
        print("Conexión con Microsoft Graph Api establecida exitosamente.")

    return account


def descargar_datos_entrenamiento(cantidad=10):
    """Extrae asuntos y cuerpos de correos para usarlos como data set."""
    print(f"Descargando {cantidad} correos...")
    print("Autenticando...")
    account = conectar_graph_api()
    mailbox = account.mailbox()
    mensajes = mailbox.get_messages(limit=cantidad)
    dataset = []

    print("Descargando mensajes...")
    for msg in mensajes:
    # guardamos solo lo util para el modelo de ML
        dataset.append({'asunto': msg.subject, 'cuerpo_previo': msg.body_preview})
    return pd.DataFrame(dataset) # Devolvemos el DataFrame

def guardar_dataset(df: pd.DataFrame, ruta_salida: str):
    """Guarda el DataFrame en un archivo CSV."""
    ruta_final = Path(ruta_salida)
    ruta_final.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta_final, index=False, encoding='utf-8')
    print(f"Dataset guardado en: {ruta_final}")


def ejecutar_extraccion(ruta_salida="data_raw.csv", cantidad=10) -> bool:
    """Función principal del módulo. Se invocará desde main.py."""
    print("Iniciando Etapa 01: Extracción de datos")
    try:
        df_correos = descargar_datos_entrenamiento(cantidad=cantidad)

        if df_correos.empty:
            print("No se encontraron correos en la bandeja de entrada.")
            return False

        guardar_dataset(df_correos, ruta_salida)
        return True

    except Exception as e:
        print(f"Error crítico en la extracción: {e}")
        return False

# Bloque de aislamiento para ejecución
if __name__ == "__main__":
    try:
        print("Iniciando descarga de datos...")
        data = descargar_datos_entrenamiento(cantidad=100) # Subimos a 100 para tener mas datos
        if data: 
            df = pd.DataFrame(data) # Convertimos la lista en una tabla (DataFrame)
            # Guardamos la tabla en una archivo CSV
            df.to_csv('dataset_correos.csv', index=False, encoding='utf-8')
            for item in data:
                print(f"Correo: {item['asunto'][:100]}...")
            print(f"\nÉxito: Tienes {len(data)} ejemplos guardados en 'dataset_correos.csv'.")
        else:
            print("No se descargaron datos.")
    except Exception as e:
        print(f"Error: {e}")