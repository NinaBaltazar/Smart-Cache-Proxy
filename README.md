# Smart Cache Proxy

Este projeto é um proxy HTTP com cache, desenvolvido em Python (Flask) e Redis, que armazena respostas de URLs requisitadas e exibe estatísticas de cache (hits/misses) em uma interface web com gráficos.

## Pré-requisitos

- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/)
- [Make](https://www.gnu.org/software/make/) (opcional, mas recomendado)
- Python 3.8+ (caso queira rodar localmente sem Docker)

## Passo a passo

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/smart_cache_proxy.git
cd smart_cache_proxy/Smart-Cache-Proxy
```
### 2. Clone o repositório

Instale as dependências (caso não use Docker)

```bash
pip3 install -r requirements.txt
```

### 3. Configure variáveis de ambiente
Crie um arquivo .env na raiz do projeto com valores padrão segue exemplo:

```bash
REDIS_HOST=localhost
REDIS_PORT=6379
DEFAULT_TTL=60
```
### 4. Suba o ambiente com Docker Compose

```bash
make build
make up
```
### 5. Popule o cache e teste
Para popular o cache com exemplos e simular hits/misses, execute:

```bash
make populate
```
### 6. Acesse a interface de status
Abra http://localhost:5001/status no navegador para ver as estatísticas e gráficos de cache.



