import subprocess
import os
import sys

def build_maven_project(project_dir):
    print(project_dir)
    pom_path = os.path.join(project_dir, "pom.xml")
    if not os.path.isdir(project_dir):
        print(f"❌ La ruta no existe o no es un directorio: {project_dir}")
        return
    result = subprocess.run(
        ["mvn", "-f", pom_path, "clean", "install", "-U", "-DskipTests", "-Dorg.slf4j.simpleLogger.defaultLogLevel=error"],
        text=True
    )
    # result = subprocess.run(
    #     ["mvn", "clean", "install", "-DskipTests" , "-Dorg.slf4j.simpleLogger.defaultLogLevel=error"],
    #     cwd=project_dir,
    #     shell=True,
    #     text=True
    # )
    
    

    if result.returncode != 0:
        print("❌ Maven falló:")
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)
    else:
        print("✅ Maven ejecutado correctamente.")
        print(result.stdout)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python build_project.py <ruta_a_proyecto>")
    else:
        build_maven_project(sys.argv[1])