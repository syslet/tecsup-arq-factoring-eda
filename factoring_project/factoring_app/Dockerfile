FROM python:3.10-slim
WORKDIR /app

# Copiar requirements desde la raíz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la carpeta factoring_app como paquete
COPY . .

# Ejecutar como paquete
EXPOSE 5000
CMD ["python", "-m", "factoring_app"]
