

# Limpieza con NLTK

import pandas as pd
import re
# Nuevo nltk
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize  # importante

nltk.download('punkt')
nltk.download('punkt_tab')# Para el tokenizador
# Descargamos las palabras vacias solo la primera vez
nltk.download('stopwords')
stop_words = set(stopwords.words('spanish'))

def limpiar_texto_y_tokenizar(texto):
    # Esto quita enlaces, caracteres especiales y lo pone todo en minúsculas
    texto = str(texto).lower()
    texto = re.sub(r'http\S+|www\S+|https\S+', '', texto, flags=re.MULTILINE) #quita linsk
    texto = re.sub(r'\W', ' ', texto) # Quita símbolos raros

    ### Esto es un codigo en caso de que no quieras el "TOKENIZADOR"###
    # Quitar "Stopwords" (Palabras que no aportan nada)
    # palabras = texto.split()
    # palabras_filtradas = [w for w in palabras if w not in stop_words]
    # return " ".join(palabras_filtradas)

    # TOKENIZACION: Corta el texto en trozos
    tokens = word_tokenize(texto)

    # Filtrado de Stopwords sobre los tokens
    tokens_limpios = [w for w in tokens if w not in stop_words]

    return tokens_limpios # Devolvemos una LISTA, no un string

# cargamos lo que descargaste antes
df = pd.read_csv('dataset_correos.csv')
df['cuerpo_previo'] = df['cuerpo_previo'].apply(limpiar_texto_y_tokenizar)
 
print(df[['asunto', 'cuerpo_previo']].head())

# Guarda el resultado limpio en un nuevo archivo para tu modelo
df.to_csv('dataset_limpio_ml.csv', index=False)
print("\nÉxito! NLTK ha eliminado las palabras innecesarias. Datos limpios guardados en 'dataset_limpio_ml.csv'") 