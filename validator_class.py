import os
import fnmatch
import sys
import chardet

# Define the words to search for in .class files
java_search_terms = ['Encoders.bean','jdbc'] #jdbc is only for test


problems=[]

# Define the words to exclude from the search
exclusion_terms = ['fasterxml']
def detectar_codificacion(file_path, bytes_to_read=1000):
    with open(file_path, 'rb') as f:
        raw_data = f.read(bytes_to_read)
    return chardet.detect(raw_data)



# Function to search for terms in a file
def search_in_file(file_path, search_terms):
    encode = detectar_codificacion(file_path)
    with open(file_path, 'r', encoding=encode['encoding'],errors='replace') as file:
        for i, line in enumerate(file):
            lower_line = line.lower()
            if any(exclusion.lower() in lower_line for exclusion in exclusion_terms):
                continue  # Skip lines with exclusion terms
            for term in search_terms:
                if term.lower() in lower_line:
                    print(f"Coincidencia encontrada {file_path}, linea {i + 1}: {term}")
                    problems.append(f"Coincidencia encontrada {file_path}, linea {i + 1}: {term}")
                    continue
                    #return True
    return False

# Function to search through .java files in the Maven project
def search_java_files(project_root):
    for root, dirs, files in os.walk(project_root):
        for file in fnmatch.filter(files, "*.class"):
            file_path = os.path.join(root, file)
            if search_in_file(file_path, java_search_terms):
                return True
    return False

def createFile():
    with open("problems.txt", "w", encoding="utf-8") as f:
        for linea in problems:
            f.write(linea + "\n")

# Main function to check the Maven project
def check_maven_project(project_root):
    if search_java_files(project_root):
        print("Se encuentran valores coincidentes con tecnologias deprecadas en la arquitectura LRBA \nError de coincidencia en fichero .java ")
        print("1")
        return 1

    createFile()
    #Script close with 0 if the status is succesfull
    return 0
   

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("INFORMACION DE USO: Por favor indicar la ruta del proyecto a auditar por parametro")
    print("Argument received to audit ", sys.argv[1])
    project_root = sys.argv[1]
    check_maven_project(project_root)