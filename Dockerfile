# Use uma imagem base oficial do Python
FROM python:3.11

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação
COPY . .

# Exponha a porta que a aplicação irá rodarW
EXPOSE 2133

# Comando para iniciar a aplicação
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "2133"]
