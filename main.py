from scripts import process 
from scripts import request
from scripts import clone
from scripts import prepare
from scripts import final
from scripts import ScriptArtefactory
from scripts import ScriptExcel
import sys

def main():
    if len(sys.argv) < 2:
        print("❌ Error: Debes indicar los parametros de ejecución.")
        print("Ejemplo: python main.py colombia latest")
        sys.exit(1)
    input_filter = sys.argv[1] if len(sys.argv) > 1 else None
    modo_latest = len(sys.argv) > 2 and sys.argv[2].lower() == "latest"
    prepare.init() 
    ScriptArtefactory.run(input_filter, modo_latest)
    ScriptExcel.generar_total()
    data = request.create_request()
    # print("data:______________",data)
    process.process_data(data)
    # clone.clone()  
    final.execute()      

    
if __name__ == "__main__":
    main()
