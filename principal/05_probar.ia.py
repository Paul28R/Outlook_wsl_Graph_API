 
import joblib
import re

# 1. Cargar el modelo y el vectorizador
modelo = joblib.load('modelo_correos.pkl')
vectorizador = joblib.load('vectorizador.pkl')

def limpiar_texto_simple(texto):
    texto = str(texto).lower()
    texto = re.sub(r'\w',' ', texto)
    return texto

def predecir_categoria():
    print("\n--- TESTER DE INTELIGENCIA ARTIFICIAL ---")
    while True:
        nuevo_correo = input("\nEscribe el cuerpo de un correo (o 'salir'): ")

        if nuevo_correo.lower() == 'salir':
            break

        # 2. Limpiamos y transformamos el texto igual que hicimos al entrenar
        texto_limpio = limpiar_texto_simple(nuevo_correo)
        texto_vectorizado = vectorizador.transform([texto_limpio])

        # 3. ¡LA IA PREDICE! 
        prediccion = modelo.predict(texto_vectorizado)
        probabilidad = modelo.predict_proba(texto_vectorizado).max()

        print(f" Resultado: Este correo es de categoria -> **{prediccion[0]}**")
        print(f" Confianza: {probabilidad*100:.2f}%")

if __name__ == "__main__":
    predecir_categoria()        