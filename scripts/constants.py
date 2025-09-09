from scripts import versions

FOLDER_ARTIFACTORY = 'Descargas_Atifactory'
SOURCE = './source'
MODIFIED = './modified'
PRODUCTIVE_JSON = 'productivo_data.json'
ERROR_XLSX = "errores_build.xlsx"
VERSIONS_XLSX = "cambios_versiones.xlsx"
PRODUCTIVE_XLSX = "total_productivo.xlsx"
TOTAL_XLSX = "total_descargas.xlsx"
COLOMBIA = ["_co_","co_c","kbtq","kcol","kcsn","kusu","kskr","kful","ksan","w1bd","kmol","kdmg","kpri","kpad","kcog","atau","opei"]
MEXICO = ["_mx_","mx_m"]
ARGENTINA = ["_ar_","ar_m"]
PERU = ["_pe_","pe_m"]
ARTIFACTORY_BASE = "gl-lrba-generic-local/lrba/apps/java/spark/"
ARTIFACTORY_URL = "https://artifactory.globaldevtools.bbva.com/artifactory"
ARTIFACTORY_URL_VERSION = "https://artifactory.globaldevtools.bbva.com/artifactory/gl-lrba-maven-local/com/bbva/lrba/spark-job-lrba-parent/"
ARTIFACTORY_ACCESS_TOKEN = "ARTIFACTORY_ACCESS_TOKEN"
REPORT = "reporte_comparacion.txt"
COOKIE = "COOKIE"
CLONE_ERROR_XLSX = "errores_clone.xlsx"
VERSIONES = versions.run()
PAISES = ["Seleccione...", "Colombia", "Mexico", "Argentina", "Peru"]
ITEM_SEARCH= {
    "colombia": "-co-",
    "mexico": "-mx-",
    "argentina": "-ar-",
    "peru": "-pe-",
}
HEIGHT_ITEMS = 330 #Utilizado en estilos
COOKIE_PDF =  "cookie.pdf"