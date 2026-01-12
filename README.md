# Social Media Downloader Microservice 🎥

Um microsserviço de alta performance (API) construído com **FastAPI** e **yt-dlp** para baixar e processar vídeos de redes sociais (YouTube, Instagram, TikTok, etc.).

Este projeto foi desenhado para atuar como um **Sidecar Service** em orquestradores de fluxo (como **n8n**), resolvendo problemas complexos de ingestão de mídia que ferramentas _low-code_ nativas não conseguem tratar.

## 🚀 Destaques Técnicos

* **Bypass de Bloqueios (Anti-Bot):** Implementação robusta de User-Agents e Headers para mitigar erros \`403 Forbidden\` (comum em Datacenters/Docker).
* **Normalização de Mídia:** Conversão forçada de streams DASH/HLS (.m3u8) para arquivos **.mp4** compatíveis com a maioria das APIs de IA.
* **Docker-First:** Container leve e isolado, pronto para produção.
* **Gerenciamento de Recursos:** Limpeza automática de arquivos temporários após o envio da resposta (Background Tasks).

## 🛠️ Tecnologias

* [Python 3.9](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/) (API Assíncrona)
* [yt-dlp](https://github.com/yt-dlp/yt-dlp) (Engine de extração)
* [FFmpeg](https://ffmpeg.org/) (Processamento de áudio/vídeo)
* [Docker](https://www.docker.com/)

---

## ⚙️ Como Rodar

### Pré-requisitos
* Docker e Docker Compose instalados no servidor ou máquina local.

### Opção 1: Via Linha de Comando (Docker CLI)
Ideal para testes rápidos ou execução isolada.

1.  **Construir a imagem:**
    \`\`\`bash
    docker build -t social-dl .
    \`\`\`

2.  **Rodar o container:**
    *O comando abaixo inicia o serviço na porta 8000 e configura para reiniciar automaticamente.*
    \`\`\`bash
    docker run -d -p 8000:8000 --name social-dl --restart always social-dl
    \`\`\`

### Opção 2: Via Docker Compose (Recomendado para Produção/n8n)
Ideal para manter o serviço rodando ao lado do n8n na mesma rede. Adicione este bloco ao seu \`docker-compose.yml\`:

\`\`\`yaml
version: '3.8'
services:
  social-dl:
    build: .
    container_name: social-dl
    restart: always
    ports:
      - "8000:8000"
    # Se estiver rodando junto com n8n, descomente e ajuste a rede abaixo:
    # networks:
    #   - n8n_network
\`\`\`

---

## 🔌 Documentação da API

### 1. Extrair Informações (Metadata)
Retorna dados do vídeo sem realizar o download do arquivo físico. Útil para obter título, thumbnail e duração.

* **Endpoint:** \`POST /extract_info\`
* **Content-Type:** \`application/json\`

**Body:**
\`\`\`json
{
  "url": "https://www.instagram.com/reel/C-xyz123abc/"
}
\`\`\`

### 2. Baixar Vídeo (Download & Process)
Realiza o download, une áudio/vídeo (se necessário), converte para MP4 e retorna o binário.

* **Endpoint:** \`POST /download_video\`
* **Content-Type:** \`application/json\`

**Body:**
\`\`\`json
{
  "url": "https://www.youtube.com/shorts/xyz123abc"
}
\`\`\`

**Retorno:**
* Arquivo binário (\`video/mp4\`).
* *Nota: O arquivo é deletado do servidor imediatamente após o envio para economizar espaço.*

---

## 🤖 Integração com n8n

Para consumir este serviço dentro de um workflow do n8n:

1.  Adicione um node **HTTP Request**.
2.  **Method:** \`POST\`.
3.  **URL:**
    * Se usar Docker Network (Sidecar): \`http://social-dl:8000/download_video\`
    * Se usar IP externo/Tunel: \`http://SEU_IP:8000/download_video\`
4.  **Body Content Type:** JSON.
5.  **Body Parameters:** \`{"url": "LINK_DO_VIDEO"}\`.
6.  **Response Format:** Selecione **File** (ou Binary).

---

## 📝 Licença

Este projeto é de código aberto (Open Source). Sinta-se livre para usar e modificar.
EOF
