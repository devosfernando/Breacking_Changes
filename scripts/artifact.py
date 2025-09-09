import os
import time
import requests
import pandas as pd
from datetime import datetime
from collections import defaultdict
from scripts import constants

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x, **kwargs: x


def obtener_identificador_base(nombre_archivo):
    partes = nombre_archivo.split('-')
    if len(partes) >= 6:
        return '-'.join(partes[:5])  # Ajusta según tu patrón real
    return nombre_archivo


def run(input_filter, modo_latest=True):
    start_time = time.time()

    artifactory_url = constants.ARTIFACTORY_URL.rstrip("/")
    repo_base = constants.ARTIFACTORY_BASE.rstrip("/")
    access_token = os.getenv(constants.ARTIFACTORY_ACCESS_TOKEN)
    headers = {"Authorization": f"Bearer {access_token}"}

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
    print(f"🔍 Filtros de entrada: {input_filters}")

    script_dir = os.path.dirname(__file__)
    download_root = os.path.join(script_dir, constants.FOLDER_ARTIFACTORY)
    os.makedirs(download_root, exist_ok=True)

    # 🔹 Pedimos todos los archivos del repo en una sola llamada
    url = f"{artifactory_url}/api/storage/{repo_base}?list&deep=1"
    print(f"🌐 Consultando API: {url}")
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    files = resp.json().get("files", [])
    print(f"📦 Archivos totales encontrados: {len(files)}")

    # 🔹 Agrupamos por carpeta
    carpetas = defaultdict(list)
    for f in tqdm(files, desc="🔎 Filtrando"):
        name = f["uri"].lstrip("/")
        if not name.endswith(".jar"):
            continue

        # Artifactory entrega fecha como string ISO8601 → convertir
        fecha_str = f.get("lastModified")
        if fecha_str:
            fecha_mod = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            fecha_mod = datetime.min

        # Carpeta = lo que esté antes del primer slash
        parts = name.split("/", 1)
        if len(parts) < 2:
            continue
        folder_name, file_name = parts

        # Filtrar por input_filters
        if input_filters and not any(filtro in folder_name for filtro in input_filters):
            continue

        carpetas[folder_name].append((file_name, fecha_mod))

    # 🔹 Procesamos cada carpeta filtrada
    for folder_name, archivos in carpetas.items():
        print(f"\n📂 Procesando carpeta: {folder_name}")

        datos_excel = []
        archivos_recientes = {}

        for file_name, fecha_mod in archivos:
            base = obtener_identificador_base(file_name)

            if modo_latest:
                if base not in archivos_recientes or fecha_mod > archivos_recientes[base]["fecha"]:
                    archivos_recientes[base] = {"fecha": fecha_mod}
            else:
                datos_excel.append({
                    "Archivo": base.upper(),
                    "Fecha de Modificación": fecha_mod.strftime('%Y-%m-%d %H:%M:%S')
                })

        if modo_latest:
            for base, info in archivos_recientes.items():
                datos_excel.append({
                    "Archivo": base.upper(),
                    "Fecha de Modificación": info["fecha"].strftime('%Y-%m-%d %H:%M:%S')
                })

        if datos_excel:
            download_dir = os.path.join(download_root, folder_name)
            os.makedirs(download_dir, exist_ok=True)

            df = pd.DataFrame(datos_excel)
            excel_path = os.path.join(download_dir, f'descargas {folder_name}.xlsx')
            df.to_excel(excel_path, index=False, sheet_name='Archivos Descargados')
            print(f"📄 Excel generado: {excel_path}")

    print(f"\n✅ Finalizado en {time.time() - start_time:.2f} segundos.")


if __name__ == "__main__":
    import sys
    input_filter = sys.argv[1] if len(sys.argv) > 1 else None
    modo_latest = True
    run(input_filter, modo_latest)
