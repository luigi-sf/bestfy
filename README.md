# 🎵 Spotify Scraper & Data Platform

Aplicação fullstack para **extração, processamento e disponibilização de dados do Spotify**, utilizando scraping automatizado, API performática e interface moderna.

---

## 🚀 Tecnologias

### 🔎 Scraping
- Scrapy  
- Playwright  

### ⚙️ Backend
- FastAPI  
- Python  
- Poetry  
- JWT + JTI  
- Blacklist de tokens  
- RBAC (controle de acesso por roles)  

### 🎨 Frontend
- React  
- Tailwind CSS  

---

## 📦 Funcionalidades

### 🔍 Scraping
- Extração de artistas, álbuns e músicas  
- Navegação automatizada com Playwright  
- Pipeline de processamento de dados  

### 🔐 Autenticação & Segurança
- Login e cadastro  
- JWT com identificador único (JTI)  
- Blacklist para invalidação de tokens  
- Controle de acesso com roles (RBAC)  

### 📊 API
- Listagem de artistas  
- Listagem de álbuns  
- Listagem de músicas  
- Estrutura escalável em camadas  

### 💻 Frontend
- Interface moderna e responsiva  
- Consumo da API  
- Gerenciamento de estado  

---

## 🧠 Arquitetura


scraper/
├── spiders/
├── pipelines/

backend/
├── app/
│ ├── routes/
│ ├── services/
│ ├── repositories/
│ ├── models/
│ └── core/

frontend/
├── src/
│ ├── components/
│ ├── pages/
│ ├── hooks/
│ └── services/


---

## ⚙️ Como rodar o projeto

### 1️⃣ Clone o repositório

bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo

🐍 Backend (FastAPI + Poetry + Makefile)
Instalar dependências
cd backend
poetry install
Rodar aplicação
make start

🔎 Scraper (Scrapy + Playwright)
cd scraper
poetry install
scrapy crawl nome_do_spider

🎨 Frontend
cd frontend
npm install
npm run dev

🔐 Autorização (Roles)
USER → acesso padrão
ADMIN → acesso administrativo


🤖 Melhorias Futuras
Sistema de recomendação com Machine Learning
Dashboard analítico
Busca avançada
Sistema de favoritos
Deploy com Docker
Automação de scraping


👨‍💻 Autor

Luigi Felicio 🚀
