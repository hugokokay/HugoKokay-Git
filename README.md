# Criação de imagem para Aplicação em Conteiner

Containerizar um website estático (HTML, CSS e JavaScript) usando usando dockerfile do Docker.

### Conteinerização?
- **Portabilidade**: Seu site funcionará da mesma forma em qualquer ambiente
- **Isolamento**: Elimina problemas de "funciona na minha máquina"
- **Escalabilidade**: Base para futuras implementações mais complexas
- **Padrão da Indústria**: Docker é amplamente utilizado no mercado

### Ferramentas Necessárias

#### 1. **Docker Desktop**
- **Windows/Mac**: Baixe em [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: Instale via terminal:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

Para verificar a instalação:
```bash
docker --version
```
#### 2. **Editor de Código**
- Recomendado: [Visual Studio Code](https://code.visualstudio.com/)
- Extensões úteis: Docker, AWS Toolkit

## 📦 Fase 1: Preparação do Ambiente Local

### Passo 1.1: Verificar estrutura do projeto

Navegue até o diretório do seu projeto:
```bash
cd caminho/para/seu/projeto
ls -la
```

Você deve ver a pasta `website/` com seus arquivos:
```bash
ls -la website/
```


### Passo 1.2: Testar o website localmente (opcional)

Você pode abrir o `index.html` diretamente no navegador para verificar se está funcionando:
```bash
# No Mac
open website/index.html

# No Linux
xdg-open website/index.html

# No Windows (PowerShell)
start website/index.html
```


---

## 🐳 Fase 2: Containerização com Docker

### Passo 2.1: Criar o Dockerfile

Na raiz do projeto (mesmo nível da pasta `website/`), crie um arquivo chamado `Dockerfile`:

```bash
touch Dockerfile
```

### Passo 2.2: Escrever o Dockerfile

Abra o Dockerfile no seu editor e adicione:

```dockerfile
# Imagem base - Nginx Alpine (leve e eficiente)
FROM nginx:alpine

# Copia os arquivos do website para o diretório do Nginx
COPY website/ /usr/share/nginx/html/

# Expõe a porta 80 (documentação - não abre a porta realmente)
EXPOSE 80

# Comando padrão quando o container iniciar
CMD ["nginx", "-g", "daemon off;"]
```

#### 🎓 Entendendo cada linha:

- **FROM nginx:alpine**: Define a imagem base. Alpine é uma versão Linux super leve
- **COPY**: Copia arquivos do host para dentro da imagem
- **EXPOSE**: Documenta qual porta o container usa
- **CMD**: Define o comando padrão ao iniciar o container

*[Espaço para print: Dockerfile criado no editor]*

### Passo 2.3: Construir a imagem Docker

No terminal, na raiz do projeto, execute:

```bash
docker build -t meu-website:v1.0 .
```

#### 🎓 Entendendo o comando:
- **docker build**: Comando para construir uma imagem
- **-t meu-website:v1.0**: Tag (nome:versão) da imagem
- **.**: Contexto de build (diretório atual)

Você verá a saída do processo de build:
```
[+] Building 10.5s (8/8) FINISHED
 => [internal] load build definition from Dockerfile
 => transferring dockerfile: 370B
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/nginx:alpine
 => [1/3] FROM docker.io/library/nginx:alpine
 => [2/3] RUN rm -rf /usr/share/nginx/html/*
 => [3/3] COPY website/ /usr/share/nginx/html/
 => exporting to image
 => naming to docker.io/library/meu-website:v1.0
```


### Passo 2.4: Verificar a imagem criada

```bash
docker images
```

Você deve ver sua imagem listada:
```
REPOSITORY     TAG       IMAGE ID       CREATED          SIZE
meu-website    v1.0      abc123def456   30 seconds ago   23.5MB
```


---

## 🧪 Fase 3: Teste Local do Container

### Passo 3.1: Executar o container localmente

```bash
docker run -d -p 8080:80 --name meu-website-container meu-website:v1.0
```

#### 🎓 Entendendo o comando:
- **docker run**: Cria e executa um container
- **-d**: Executa em background (detached)
- **-p 8080:80**: Mapeia porta 8080 do host para porta 80 do container
- **--name**: Nome do container
- **meu-website:v1.0**: Imagem a ser usada

### Passo 3.2: Verificar se o container está rodando

```bash
docker ps
```

Você verá algo como:
```
CONTAINER ID   IMAGE              COMMAND                  CREATED         STATUS         PORTS                  NAMES
xyz789abc123   meu-website:v1.0   "nginx -g 'daemon..."   10 seconds ago  Up 9 seconds   0.0.0.0:8080->80/tcp   meu-website-container
```


### Passo 3.3: Testar no navegador

Abra seu navegador e acesse:
```
http://localhost:8080
```

Você deve ver seu website funcionando! 🎉


### Passo 3.4: Verificar logs do container (opcional)

```bash
docker logs meu-website-container
```

### Passo 3.5: Parar e remover o container de teste

```bash
# Parar o container
docker stop meu-website-container

# Remover o container
docker rm meu-website-container
```

---


