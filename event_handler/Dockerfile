# event_handler/Dockerfile
# Use uma imagem base oficial do Python
FROM python:3.11

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos e instale as dependências
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação
COPY . /app

# Exponha a porta que a aplicação irá rodar
EXPOSE 8313

# Comando para iniciar a aplicação
CMD ["uvicorn", "event_handler.app:app", "--host", "0.0.0.0", "--port", "8313"]
