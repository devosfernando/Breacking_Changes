import os
from artifactory import ArtifactoryPath
from scripts import constants

def run():  

    # Configuración de Artifactory
    artifactory_url = constants.ARTIFACTORY_URL_VERSION
    access_token = os.getenv(constants.ARTIFACTORY_ACCESS_TOKEN) 

    # Directorio del script y carpeta de descargas
    script_dir = os.path.dirname(__file__)
    download_root = os.path.join(script_dir, constants.FOLDER_ARTIFACTORY)
    os.makedirs(download_root, exist_ok=True)

    # Conectar con Artifactory
    base_path = ArtifactoryPath(f"{artifactory_url}", token=access_token)

    arr = ["Seleccione..."]
    for folder in base_path:
         txt = str(folder)
         llave = txt.split("/")[-1]
         arr.append(llave)

    arr.pop()
    return arr

