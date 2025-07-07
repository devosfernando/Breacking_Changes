# Imagen base oficial de Python
FROM python:3.11-slim

# Instala Maven y dependencias necesarias
RUN apt-get update && apt-get install -y maven openjdk-17-jdk && apt-get clean

# Create .m2 directory for Maven settings
COPY settings.xml ./etc/maven/settings.xml

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto al ejecutar el contenedor
CMD ["python", "main.py"]