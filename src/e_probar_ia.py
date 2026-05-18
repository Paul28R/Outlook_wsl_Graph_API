import os
import re

import joblib


def cargar_modelo(modelo_path="modelo_correos.pkl", vectorizador_path="vectorizador.pkl"):
    if not os.path.exists(modelo_path):
        raise FileNotFoundError(f"No se encontró el modelo: {modelo_path}")
    if not os.path.exists(vectorizador_path):
        raise FileNotFoundError(f"No se encontró el vectorizador: {vectorizador_path}")

    modelo = joblib.load(modelo_path)
    vectorizador = joblib.load(vectorizador_path)
    return modelo, vectorizador


def limpiar_texto_simple(texto):
    texto = str(texto).lower()
    texto = re.sub(r'[^a-záéíóúüñ0-9\s]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto


def predecir_categoria(
    modelo_path="modelo_correos.pkl",
    vectorizador_path="vectorizador.pkl",
):
    modelo, vectorizador = cargar_modelo(modelo_path, vectorizador_path)

    print("\n--- TESTER DE INTELIGENCIA ARTIFICIAL ---")
    while True:
        nuevo_correo = input("\nEscribe el cuerpo de un correo (o 'salir'): ")

        if nuevo_correo.lower() == 'salir':
            break

        texto_limpio = limpiar_texto_simple(nuevo_correo)
        texto_vectorizado = vectorizador.transform([texto_limpio])

        prediccion = modelo.predict(texto_vectorizado)
        probabilidad = modelo.predict_proba(texto_vectorizado).max()

        print(f" Resultado: Este correo es de categoria -> **{prediccion[0]}**")
        print(f" Confianza: {probabilidad*100:.2f}%")


if __name__ == "__main__":
    predecir_categoria()
