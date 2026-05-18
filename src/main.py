from pathlib import Path

from principal.procesar_datos import limpiar_datos
from b_procesar_datos import procesar_con_nltk
from c_etiquetar_datos import etiquetar
from d_entrenar_ia import entrenar_modelo
from e_probar_ia import predecir_categoria

ROOT = Path(__file__).resolve().parent


def seleccionar_procesador():
    print("\nSelecciona el método de procesamiento:")
    print("1) principal/procesar_datos.py  (recomendado)")
    print("2) b_procesar_datos.py  (método alternativo)")
    return input("Opción [1-2]: ").strip()


def ejecutar_procesamiento():
    opcion = seleccionar_procesador()
    if opcion == "2":
        df = procesar_con_nltk(
            input_path=str(ROOT / "dataset_correos.csv"),
            output_path=str(ROOT / "dataset_limpio_ml.csv"),
            texto_col="cuerpo_previo",
        )
    else:
        df = limpiar_datos(
            input_path=str(ROOT / "dataset_correos.csv"),
            output_path=str(ROOT / "dataset_limpio_ml.csv"),
            texto_col="cuerpo_previo",
        )

    print(f"\nProcesamiento completo. Archivo guardado en: {ROOT / 'dataset_limpio_ml.csv'}")
    print(f"Filas procesadas: {len(df)}")


def ejecutar_etiquetado():
    etiquetar()


def ejecutar_entrenamiento():
    entrenar_modelo(
        input_path=str(ROOT / "dataset_etiquetado.csv"),
        modelo_path=str(ROOT / "modelo_correos.pkl"),
        vectorizador_path=str(ROOT / "vectorizador.pkl"),
    )


def ejecutar_pruebas():
    predecir_categoria(
        modelo_path=str(ROOT / "modelo_correos.pkl"),
        vectorizador_path=str(ROOT / "vectorizador.pkl"),
    )


def mostrar_menu():
    print("\n=== MENU PRINCIPAL ===")
    print("1) Procesar datos")
    print("2) Etiquetar datos")
    print("3) Entrenar IA")
    print("4) Probar IA")
    print("5) Ejecutar pipeline completo (procesar + entrenar)")
    print("0) Salir")
    return input("Selecciona una opción: ").strip()


def main():
    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            ejecutar_procesamiento()
        elif opcion == "2":
            ejecutar_etiquetado()
        elif opcion == "3":
            ejecutar_entrenamiento()
        elif opcion == "4":
            ejecutar_pruebas()
        elif opcion == "5":
            ejecutar_procesamiento()
            ejecutar_entrenamiento()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
