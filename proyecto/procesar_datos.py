

# Limpieza con NLTK

import pandas as pd
import re

def limpiar_texto(texto):
    # Esto quita enlaces, caracteres especiales y lo pone todo en minúsculas
    texto = str(texto).lower()
    texto = re.sub(r'http\S+|www\S+|https\S+', '', texto, flags=re.MULTILINE) #quita linsk
    texto = re.sub(r'\W', ' ', texto) # Quita símbolos raros
    return texto

# cargamos lo que descargaste antes
df = pd.read_csv('dataset_correos.csv')
df['cuerpo_previo'] = df['cuerpo_previo'].apply(limpiar_texto)
 
print(df[['asunto', 'cuerpo_previo']].head())

# Guarda el resultado limpio en un nuevo archivo para tu modelo
df.to_csv('dataset_limpio_ml.csv', index=False)
print("\nÉxito! Datos limpios guardados en 'dataset_limpio_ml.csv'")