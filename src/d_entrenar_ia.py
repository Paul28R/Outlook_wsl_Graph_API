import os

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


def preparar_texto(texto):
    if isinstance(texto, (list, tuple)):
        return " ".join(str(token) for token in texto)
    if pd.isna(texto):
        return ""
    return str(texto)


def entrenar_modelo(
    input_path="dataset_etiquetado.csv",
    modelo_path="modelo_correos.pkl",
    vectorizador_path="vectorizador.pkl",
):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"No se encontró el archivo: {input_path}")

    df = pd.read_csv(input_path)
    df = df.dropna(subset=["categoria"])

    if df.empty:
        raise ValueError("No hay datos etiquetados disponibles para entrenar.")

    df["cuerpo_previo"] = df["cuerpo_previo"].apply(preparar_texto)

    vectorizador = TfidfVectorizer()
    X = vectorizador.fit_transform(df["cuerpo_previo"])
    y = df["categoria"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = MultinomialNB()
    modelo.fit(X_train, y_train)

    print("--- Evaluación del modelo ---")
    predicciones = modelo.predict(X_test)
    print(classification_report(y_test, predicciones))

    joblib.dump(modelo, modelo_path)
    joblib.dump(vectorizador, vectorizador_path)
    print(f"\nModelo entrenado y guardado como '{modelo_path}'")


if __name__ == "__main__":
    entrenar_modelo()
