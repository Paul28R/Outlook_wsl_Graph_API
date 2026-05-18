# 📧 Outlook ML Classifier (WSL: Ubuntu)

Este proyecto utiliza la **Microsoft Graph API** para extraer correos electrónicos de Outlook y aplicar un modelo de **Machine Learning** para su clasificación automática. Está diseñado para ejecutarse en un entorno Linux (WSL/Ubuntu).

## 🚀 Características

- **Extracción de datos**: Conecta con Outlook vía Microsoft Graph API para obtener correos electrónicos.
- **Procesamiento de texto**: Limpieza y tokenización usando NLTK (en español).
- **Clasificación ML**: Modelo de Naive Bayes con vectorización TF-IDF.
- **Etiquetado manual**: Interfaz simple para etiquetar datos de entrenamiento.
- **Contenedorización**: Dockerfile para ejecutar en entornos aislados.
- **Autenticación OAuth2**: Uso de MSAL/O365 para autenticación segura.

---

## 📋 Prerrequisitos

- **Python 3.11+**
- **Cuenta de Microsoft/Outlook** con correos electrónicos
- **Suscripción a Azure AD** (para registrar la aplicación)
- **WSL/Ubuntu** o entorno Linux
- **Docker** (opcional)

---

## ⚙️ Configuración Inicial

### 1. Clonar y configurar entorno

```bash
git clone <tu-repositorio>
cd Outlook_wsl_Graph_API
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con:

```env
CLIENT_ID=tu_application_client_id_aqui
SECRET_VALUE=tu_client_secret_value_aqui
```

Este archivo se mantiene fuera del control de versiones.

---

## 📂 Estructura de archivos relevante

```
Outlook_wsl_Graph_API/
├── Dockerfile
├── README.md
├── requirements.txt
├── .env
├── src/
│   ├── __init__.py
│   ├── a_extractor_ml.py
│   ├── c_etiquetar_datos.py
│   ├── d_entrenar_ia.py
│   ├── e_probar_ia.py
│   ├── main.py
│   └── principal/
│       ├── __init__.py
│       └── procesar_datos.py
└── proyecto/
```

---

## 📊 Flujo de trabajo

### 1) Extracción de datos

Extrae correos desde Outlook y guarda un CSV con asunto y cuerpo previo.

```bash
python3 src/a_extractor_ml.py
```

Salida esperada:
- `dataset_correos.csv`

### 2) Procesamiento de datos

Limpia y tokeniza el texto para generar el dataset listo para etiquetar.

```bash
python3 src/principal/procesar_datos.py
```

Salida esperada:
- `dataset_limpio_ml.csv`

### 3) Etiquetado de datos

Asigna manualmente categorías a los correos.

```bash
python3 src/c_etiquetar_datos.py
```

Salida esperada:
- `dataset_etiquetado.csv`

### 4) Entrenamiento del modelo

Entrena el modelo Naive Bayes usando los datos etiquetados.

```bash
python3 src/d_entrenar_ia.py
```

Salida esperada:
- `modelo_correos.pkl`
- `vectorizador.pkl`

### 5) Probar el modelo

Verifica la clasificación en tiempo real con texto de ejemplo.

```bash
python3 src/e_probar_ia.py
```

---

## 🧠 ¿Qué hace cada archivo?

- `src/a_extractor_ml.py`: extrae datos desde Outlook y guarda `dataset_correos.csv`.
- `src/principal/procesar_datos.py`: limpia y tokeniza el texto, guarda `dataset_limpio_ml.csv`.
- `src/c_etiquetar_datos.py`: etiqueta datos manualmente y guarda `dataset_etiquetado.csv`.
- `src/d_entrenar_ia.py`: entrena el modelo y guarda los archivos `modelo_correos.pkl` y `vectorizador.pkl`.
- `src/e_probar_ia.py`: carga el modelo guardado y permite predecir la categoría de un nuevo texto.
- `src/main.py`: punto de entrada principal en desarrollo para orquestar el pipeline.

---

## 🔧 Notas importantes

- El archivo `.env` debe contener `CLIENT_ID` y `SECRET_VALUE`.
- Si no tienes tokens válidos, `src/a_extractor_ml.py` solicitará la autenticación en el navegador.
- Los datos intermedios se guardan en la raíz del proyecto como CSV.

---

## 🐳 Uso con Docker

### Construir imagen

```bash
docker build -t outlook-ml-classifier .
```

### Ejecutar contenedor

```bash
docker run --rm -v $(pwd):/app outlook-ml-classifier python3 src/a_extractor_ml.py
```

Ajusta el volumen según tus rutas.

---

## 🚀 Siguientes pasos

- Asegurar que `src/main.py` importe los módulos correctos.
- Mejorar el etiquetado con interfaz más amigable.
- Añadir carpetas `data/` y `models/` si quieres mantener los archivos organizados.
