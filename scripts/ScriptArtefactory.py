import os
import sys
from artifactory import ArtifactoryPath
from collections import defaultdict
from datetime import datetime
import pandas as pd
from scripts import constants

def run(input_filter, modo_latest):  

    # Configuración de Artifactory
    artifactory_url = constants.ARTIFACTORY_URL
    repo_base = constants.ARTIFACTORY_BASE
    access_token = os.getenv(constants.ARTIFACTORY_ACCESS_TOKEN)

        
    options = {
        "colombia": constants.COLOMBIA,
        "mexico": constants.MEXICO,
        "peru": constants.PERU,
        "argentina": constants.ARGENTINA
    }

    input_filters = options.get(
        input_filter.lower(),
        [f.strip() for f in input_filter.split(",") if f.strip()]
    )
    print(input_filters)

    # Directorio del script y carpeta de descargas
    script_dir = os.path.dirname(__file__)
    download_root = os.path.join(script_dir, constants.FOLDER_ARTIFACTORY)
    os.makedirs(download_root, exist_ok=True)

    # Función para extraer el identificador base del archivo
    def obtener_identificador_base(nombre_archivo):
            partes = nombre_archivo.split('-')
            if len(partes) >= 6:
                return '-'.join(partes[:5])  # Ajusta según el patrón real de tus archivos
            return nombre_archivo

    # Conectar con Artifactory
    base_path = ArtifactoryPath(f"{artifactory_url}/{repo_base}", token=access_token)
    # for folder_name in lista_de_folders:
    #     if input_filters and not any(f in folder_name for f in input_filters):
    #         continue
    # Procesar carpeta por carpeta
    print("---------------------------INPUT-FILTERS--------------------",input_filters)
    for folder in base_path:
        if folder.is_dir():
            folder_name = folder.name

            #if input_filter and input_filter not in folder_name:
            if input_filters and not any(f in folder_name for f in input_filters):
                continue

            print(f"\n📂 Procesando carpeta: {folder_name}")
            repo_path = f"{repo_base}{folder_name}/"
            artifact_path = ArtifactoryPath(f"{artifactory_url}/{repo_path}", token=access_token)

            archivos_recientes = defaultdict(lambda: {"fecha": datetime.min, "artifact": None})
            archivos_a_descargar = []

            for artifact in artifact_path:
                if artifact.is_file() and artifact.name.endswith('.jar'):
                    file_info = artifact.stat()
                    fecha_modificacion = file_info.mtime.replace(tzinfo=None)
                    identificador_base = obtener_identificador_base(artifact.name)

                    if modo_latest:
                        if fecha_modificacion > archivos_recientes[identificador_base]["fecha"]:
                            archivos_recientes[identificador_base] = {"fecha": fecha_modificacion, "artifact": artifact}
                    else:
                        archivos_a_descargar.append(artifact)

            if modo_latest:
                archivos_a_descargar = [info["artifact"] for info in archivos_recientes.values()]

            datos_excel = []

            for artifact in archivos_a_descargar:
                if artifact:
                    download_dir = os.path.join(download_root, folder_name)
                    os.makedirs(download_dir, exist_ok=True)
                    file_path = os.path.join(download_dir, artifact.name)
                    print(f"📥 Descargando {artifact.name} a {file_path}...")
                    try:
                        # with artifact.open() as fsrc, open(file_path, 'wb') as fdst:
                        #     fdst.write(fsrc.read())
                        # Lista excel por UUAA
                        datos_excel.append({
                            "Archivo": obtener_identificador_base(artifact.name).upper(),
                            "Fecha de Modificación": artifact.stat().mtime.strftime('%Y-%m-%d %H:%M:%S')
                        })
                    except Exception as e:
                        print(f" Error al descargar {artifact.name}: {e}")

            if datos_excel:
                df = pd.DataFrame(datos_excel)
                excel_path = os.path.join(download_dir, 'descargas ' + folder_name + '.xlsx')
                df.to_excel(excel_path, index=False, sheet_name='Archivos Descargados')
                print(f"📄 Archivo Excel generado en: {excel_path}")

    print("\n✅ Descarga completada.")

if __name__ == "__main__":
    import sys
    input_filter = sys.argv[1] if len(sys.argv) > 1 else None
    modo_latest = len(sys.argv) > 2 and sys.argv[2].lower() == "latest"
    run(input_filter, modo_latest)
