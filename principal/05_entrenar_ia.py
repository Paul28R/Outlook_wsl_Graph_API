
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import joblib # Para guardar el modelo en un archivo

# 1. Cargar tus datos etiquetados
df = pd.read_csv('dataset_etiquetado.csv')
# Eliminamos filas que no llegaste a etiquetar
df = df.dropna(subset=['categoria'])

# 2. Convertir texto a números (TF-IDF)
# Esto convierte tus listas de palabras en coordenadas matemáticas
vectorizador = TfidfVectorizer()
X = vectorizador.fit_transform(df['cuerpo_previo'])
y = df['categoria']

# 3. Dividir datos: unos para aprender (80%) y otros para examen (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Crear y entrenar el "Cerebro" (Modelo)
modelo = MultinomialNB()
modelo.fit(X_train, y_train)

# 5. Ver qué tan inteligente es nuestra IA
print("--- Evaluacion del Modelo ---")
predicciones = modelo.predict(X_test)
print(classification_report(y_test, predicciones))

# 6. GUARDAR EL MODELO (Para no repetir esto siempre)
joblib.dump(modelo, 'modelo_correos.pkl')
joblib.dump(vectorizador,  'vectorizador.pkl')
print("\n Modelo entrenado y guardado como 'modelo_correos.pkl'")