# Use a imagem base do Python
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /app

# Crie o diretório de logs
RUN mkdir -p /app/logs

# Copie o script para o diretório de trabalho
COPY log_generator.py .

# Instale Flask
RUN pip install flask

# Exponha a porta que o Flask usará
EXPOSE 5000

# Comando para executar o script
CMD ["python", "log_generator.py"]
