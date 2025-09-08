import os
import stat
from scripts import constants

def clean_readonly_and_remove(path):
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    os.chmod(file_path, stat.S_IWRITE)
                    os.remove(file_path)
                except Exception as e:
                    print(f"⚠️ Error eliminando archivo {file_path}: {e}")
            for name in dirs:
                dir_path = os.path.join(root, name)
                try:
                    os.rmdir(dir_path)
                except Exception as e:
                    print(f"⚠️ Error eliminando carpeta {dir_path}: {e}")
        try:
            os.rmdir(path)
        except Exception as e:
            print(f"⚠️ Error eliminando raíz {path}: {e}")
            

def delete_file(file):
    if os.path.isfile(file):
        os.remove(file)
        
def init():
    #---------CLEAN WORKSPACE ----------#
    clean_readonly_and_remove(constants.MODIFIED)
    clean_readonly_and_remove(constants.SOURCE)
    delete_file(constants.ERROR_XLSX)
    delete_file(constants.VERSIONS_XLSX)
    delete_file(constants.PRODUCTIVE_XLSX)
    #---------CLEAN WORKSPACE ----------#