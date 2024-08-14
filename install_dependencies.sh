#!/bin/bash

# definir a versão do Docker
DOCKER_VERSION="20.10.17"

# Verificar se o Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "Docker não está instalado."
        return 1
    fi

    INSTALLED_VERSION=$(docker --version | awk -F '[ ,]+' '{ print $3 }')

    if [ "$INSTALLED_VERSION" != "$DOCKER_VERSION" ]; then
        echo "Versão do Docker instalada ($INSTALLED_VERSION) não é a necessária ($DOCKER_VERSION)."
        return 1
    fi

    echo "Versão correta do Docker está instalada: $INSTALLED_VERSION."
    return 0
}

# Instalar o Docker
install_docker() {
    echo "Instalando o Docker versão $DOCKER_VERSION..."
    
    # Remover qualquer instalação anterior do Docker
    sudo apt-get remove -y docker docker-engine docker.io containerd runc

    # Instalar pacotes necessários para adicionar um novo repositório
    sudo apt-get update
    sudo apt-get install -y \
        ca-certificates \
        curl \
        gnupg

    # Adicionar chave GPG oficial do Docker
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

    # Adicionar repositório do Docker
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/$(. /etc/os-release && echo "$ID") \
    $(lsb_release -cs) stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    # Atualizar e instalar Docker
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    # Verificar a instalação
    if ! command -v docker &> /dev/null; then
        echo "Falha ao instalar o Docker."
        exit 1
    fi

    INSTALLED_VERSION=$(docker --version | awk -F '[ ,]+' '{ print $3 }')
    echo "Docker instalado com sucesso. Versão: $INSTALLED_VERSION."
}

# Verificar e instalar o Docker se necessário
check_docker || install_docker

echo "Todas as dependências foram instaladas com sucesso."
