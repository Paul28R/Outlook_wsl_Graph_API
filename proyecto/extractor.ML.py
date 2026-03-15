
# esto carga las variables del archivo .env load_dotenv()
import os 
import pandas as pd
from dotenv import load_dotenv
#
from pathlib import Path
# Esto busca el archivo .env un nivel arriba de donde esta el script
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# esto se utiliza para extraer los correos
from O365 import Account 


# Pegamos aqui las llaves (IDs y el secreto value cree)
CLIENT_ID = os.getenv('CLIENT_ID')
SECRET_VALUE = os.getenv('SECRET_VALUE')


def conectar_api():
    """Funcion para autenticarse con la API de Microsoft."""
    credentials = (CLIENT_ID, SECRET_VALUE)
    account = Account(credentials)

    if not account.is_authenticated:
        # Definimos la url que pusimos en Azure
        # url_nativa = 'https://login.microsoftonline.com/common/oauth2/nativeclient'
        url_choque = 'http://localhost:8080'
        # Iniciamos la autenticacion indicando que queremos que se quede en consola
        # Esto evita que el proceso expire tan rapido
        # account.authenticate(scopes=['basic','message_all'], redirect_uri=url_nativa)
        account.authenticate(scopes=['https://graph.microsoft.com/Mail.Read'],redirect_uri=url_choque)
    
    return account


def descargar_datos_entrenamiento(cantidad=10):
    """Extrae asuntos y cuerpos de correos para usarlos como data set."""
    account = conectar_api()
    mailbox = account.mailbox()
    mensajes = mailbox.get_messages(limit=cantidad)


    dataset = []
    for msg in mensajes:
    # guardamos solo lo util para el modelo de ML
        dataset.append({'asunto': msg.subject, 'cuerpo_previo': msg.body_preview})
    return dataset

if __name__ == "__main__":
    try:
        print("Iniciando descarga de datos...")
        data = descargar_datos_entrenamiento(cantidad=50) # Subimos a 50 para tener mas datos
        if data: 
            df = pd.DataFrame(data) # Convertimos la lista en una tabla (DataFrame)
            # Guardamos la tabla en una archivo CSV
            df.to_csv('dataset_correos.csv', index=False, encoding='utf-8')
            for item in data:
                print(f"Correo: {item['asunto'][:50]}...")
            print(f"\nÉxito: Tienes {len(data)} ejemplos guardados en 'dataset_correos.csv'.")
        else:
            print("No se descargaron datos.")
    except Exception as e:
        print(f"Error: {e}")