import os
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

NLTK_RESOURCES = ["punkt", "stopwords"]
SPANISH_STOPWORDS = None


def descargar_recursos_nltk():
    """Descarga los recursos de NLTK que se necesitan en tiempo de ejecución."""
    for recurso in NLTK_RESOURCES:
        nltk.download(recurso, quiet=True)


def obtener_stopwords():
    """Carga las stopwords en español una sola vez."""
    global SPANISH_STOPWORDS
    if SPANISH_STOPWORDS is None:
        descargar_recursos_nltk()
        SPANISH_STOPWORDS = set(stopwords.words("spanish"))
    return SPANISH_STOPWORDS


def limpiar_texto_y_tokenizar(texto, stop_words=None):
    """Limpia un texto y devuelve una lista de tokens sin stopwords."""
    if stop_words is None:
        stop_words = obtener_stopwords()

    texto = str(texto).lower()
    texto = re.sub(r'https?://\S+|www\.\S+', '', texto, flags=re.IGNORECASE)
    texto = re.sub(r'[^A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9\s]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()

    tokens = word_tokenize(texto, language="spanish")
    tokens_limpios = [token for token in tokens if token not in stop_words]
    return tokens_limpios


def limpiar_datos(
    input_path="dataset_correos.csv",
    output_path="dataset_limpio_ml.csv",
    texto_col="cuerpo_previo",
    columnas_salida=None,
):
    """Carga el CSV, limpia el texto y guarda el dataset procesado."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"No se encontró el archivo: {input_path}")

    df = pd.read_csv(input_path)

    if texto_col not in df.columns:
        raise ValueError(f"La columna '{texto_col}' no existe en {input_path}")

    stop_words = obtener_stopwords()
    df[texto_col] = df[texto_col].apply(lambda texto: limpiar_texto_y_tokenizar(texto, stop_words))

    if columnas_salida is not None:
        df = df.loc[:, columnas_salida]

    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    df_procesado = limpiar_datos()
    print(df_procesado[["asunto", "cuerpo_previo"]].head())
    print(f"\nÉxito! Datos guardados en '{os.path.abspath('dataset_limpio_ml.csv')}'")
