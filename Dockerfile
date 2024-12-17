FROM python:3.9-slim

# Instala dependências necessárias para Ollama e o sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Instala Ollama
RUN wget https://ollama.ai/install.sh -O - | bash

# Cria diretório para rodar o aplicativo
WORKDIR /ollama_pdf_rag

# Clona o repositório do Streamlit
RUN git clone https://github.com/tonykipkemboi/ollama_pdf_rag.git .

# Instala as dependências do Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Expõe as portas do Streamlit e Ollama
EXPOSE 8501 11434

# Baixa os modelos na inicialização do container
CMD ollama serve & \
    sleep 5 && \
    ollama pull llama2 && \
    ollama pull nomic-embed-text && \
    streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0

