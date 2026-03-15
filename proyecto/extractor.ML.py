
# esto carga las variables del archivo .env load_dotenv()
import os 
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
    account = Account(credentials, auth_flow_type='authorization', tenant_id='common')


    if not account.is_authenticated:
        # El scope 'offline_access' es para que no te pida login cada vez
                                    #'basic', 'message_all'
        account.authenticate(scopes=['https://graph.microsoft.com/Mail.Read','offline_access'])
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
        data = descargar_datos_entrenamiento()
        for item in data:
            print(f"Correo: {item['asunto'][:50]}...")
        print(f"\nÉxito: Tienes {len(data)} ejemplos para tu futuro modelo.")
    except Exception as e:
        print(f"Error: {e}")
