# Usa una imagen base de Python
FROM python:3.12.4

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos y el script de la aplicación al contenedor
# COPY requirements.txt requirements.txt
# COPY main.py main.py
# COPY templates/ templates/
# COPY static/ static/
# COPY MCI_DB.db3 MCI_DB.db3
COPY . .

# Instala las dependencias de Python
RUN pip install -r requirements.txt

# Expone el puerto en el que Flask se ejecutará
EXPOSE 5000

# Define el comando para ejecutar la aplicación
CMD ["python3", "main.py"]