
import pandas as pd
import os

def etiquetar():
    archivo_entrada = 'dataset_limpio_ml.csv'
    archivo_salida = 'dataset_etiquetado.csv'

    if not os.path.exists(archivo_entrada): 
        print("No encuentro el archivo limpio. Corre primero procesar_datos.py")
        return
    # Cargamos el dataframe
    df = pd.read_csv(archivo_entrada)

    # Si no existe la columna categoria, la creamos
    if 'categoria' not in df.columns:
        df['categoria'] = None

    print("--- Etiquetador de correos ---")
    print("Escribe la categoria para cada correo (ej: Trabajo, Social, Sistema, Spam)")
    print("Escribe 'Salir para guardar y terminar.\n")

    try:    
        for i, fila in df.iterrows():
            # Solo etiquetamos los que faltan
            if pd.isna(df.at[i, 'categoria']):
                print(f"[{i+1}/{len(df)}]Asunto: {fila['asunto']}")

                etiqueta = input("Etiqueta(Trabajo/Spam/etc): ").strip()

                if etiqueta.lower() == 'salir':
                    print("\nSaliendo y guardando...")
                    break
                
                if etiqueta:
                    df.at[i, 'categoria'] = etiqueta 
                    print("OK!")
                print("-" * 30)

    except KeyboardInterrupt:
        print("\nInterrupción forzada. Guardando progreso...")

    # Guardamos el progreso
    df.to_csv('dataset_etiquetado.csv', index=False)
    print(f"\n ¡Progreso guardado en {archivo_salida} 'dataset_etiquetado.csv'!")
    
if __name__ == "__main__":
    etiquetar()