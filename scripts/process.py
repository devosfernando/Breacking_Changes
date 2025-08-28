import pandas as pd
from packaging import version
import json
from scripts import constants

productivoName = constants.PRODUCTIVE_XLSX

def process_data(data):
    print("Processing data...\n")
    extracted_items = []

    if isinstance(data, list):
        for item in data:
            job_name = item.get("jobName")
            job_version = item.get("jobVersion")
            job_artifact = item.get("jobConfig", {}).get("artifact")
            job_ns = item.get("namespace")
            if job_name and job_version and job_artifact and job_ns.startswith("co."):
                extracted_items.append({
                    "job": job_name,
                    "version": job_version,
                    "artifact": job_artifact,
                    "namespace": job_ns
                })

        extracted = extracted_items
        df = pd.DataFrame(extracted)

        # Si hay duplicados exactos, se eliminan primero
        df = df.drop_duplicates()
        print(df)
        # Convertimos las versiones a objetos comparables
        df["version_obj"] = df["version"].apply(version.parse)

        # Ordenamos por artifact y versión descendente
        df_sorted = df.sort_values(by=["artifact", "version_obj"], ascending=[True, False])

        # Nos quedamos con la última versión por artifact
        df_latest = df_sorted.drop_duplicates(subset=["job"], keep="first")
        #df_latest = df_sorted.drop_duplicates(subset=["artifact"], keep="first")

        # Eliminamos columna auxiliar
        df_latest = df_latest.drop(columns=["version_obj"])

        df_latest.to_excel(productivoName, index=False)
        
        # Leer el Excel completo
        df = pd.read_excel(constants.PRODUCTIVE_XLSX)

        # Convertir el DataFrame a lista de diccionarios (filas completas)
        data = df.to_dict(orient="records")
        # Guardar la data en un archivo JSON temporal
        with open(constants.PRODUCTIVE_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✔ Archivo generado: {productivoName}")
    else:
        print("❌ El formato no es una lista")
