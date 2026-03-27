# 📧 Outlook ML Classifier (WSL: Ubuntu)

Este proyecto utiliza la **Microsoft Graph API** para extraer correos electrónicos de Outlook y aplicar modelos de **Machine Learning** para su clasificación automática. Está diseñado para ejecutarse en un entorno Linux (WSL/Ubuntu).

---

## Configuración en (Azure)

Para que el script extractor.ML.py funcione, debes registrar una aplicacion en Azure Portal:
1. App registration: Crea una nueva aplicacion en "Azure active Directory"
2. Permisos de API: Añade Mail.Read y User.Read (Permisos delegados)


## 📊 Flujo de Datos (Data Pipeline)

```mermaid
graph TD
    A[Microsoft Graph API] -->|extractor.ML.py| B(dataset_correos.csv)
    B -->|procesar_datos.py| C(dataset_limpio_ml.csv)
    C -->|entrenar_ia.py| D[Modelo .pkl]
    C -->|entrenar_ia.py| E[Vectorizador .pkl]
    D & E -->|probar.ia.py| F{Inferencia en Vivo}
    A -->|Auth| G[o365_token.txt]

