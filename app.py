from scripts import process 
from scripts import request
from scripts import clone
from scripts import prepare
from scripts import final
from scripts import ScriptArtefactory
from scripts import ScriptExcel
from scripts import constants

def main_execute(country,version,token):
    input_filter = country.lower()
    modo_latest =  "latest"
    item_search = ""
    
    if country in constants.ITEM_SEARCH:
        item_search = constants.ITEM_SEARCH[country]
        print(f"Found: {item_search}")

    prepare.init() 
    ScriptArtefactory.run(input_filter, modo_latest)
    ScriptExcel.generar_total()
    data = request.create_request(input_filter,token)
    process.process_data(data)
    clone.clone()  
    return final.execute(version)      
