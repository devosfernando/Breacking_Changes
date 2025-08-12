import os
import pandas as pd
from scripts import constants

def generar_total():
    download_root = os.path.join(os.path.dirname(__file__), constants.FOLDER_ARTIFACTORY)

    dataframes = []

    for folder_name in os.listdir(download_root):
        folder_path = os.path.join(download_root, folder_name)
        if os.path.isdir(folder_path):
            # Buscar el archivo Excel en la subcarpeta
            excel_file = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
            if excel_file:
                excel_path = os.path.join(folder_path, excel_file[0])
                # Leer el archivo Excel y agregar una columna con el nombre de la carpeta
                df = pd.read_excel(excel_path)
                df['Carpeta'] = folder_name
                dataframes.append(df)

    # Combinar todos los DataFrames en uno solo
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        # Guardar el DataFrame combinado en un nuevo archivo Excel
        combined_excel_path = os.path.join('', 'total_descargas.xlsx')
        combined_df.to_excel(combined_excel_path, index=False, sheet_name='Descargas Combinadas')
        print(f"📄 Archivo Excel combinado generado en: {combined_excel_path}")
    else:
        print("No se encontraron archivos Excel para combinar.")
    

if __name__ == "__main__":
    generar_total()
