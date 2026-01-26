# 🛒 Loja Online

Projeto **fullstack** de uma loja online, desenvolvido com **FastAPI** no backend e **React + Vite + TypeScript** no frontend.  
Banco de dados: **MySQL via Docker**.  

**Objetivo**: praticar boas práticas de desenvolvimento, testes automatizados e deploy com CI/CD, explorando o ciclo completo de um app moderno.

---

## 🚀 Tecnologias

- **Backend**: FastAPI + SQLAlchemy  
- **Frontend**: React + Vite + TypeScript  
- **Banco**: MySQL (Docker)  
- **Testes**: Pytest (backend), Jest + React Testing Library (frontend)  
- **Deploy**: Docker Compose  

---

## 📆 Plano de Desenvolvimento (11 Etapas)

### ✅ Concluído

**Etapa 1 — Infraestrutura**  
- Criar Dockerfile e docker-compose.yml.  
- Subir containers: MySQL, FastAPI, React.  
- Garantir comunicação entre serviços e banco inicializado.  
➡️ Afeta: toda a base do projeto, pois sem infraestrutura nada roda.

**Etapa 2 — Modelos e Banco (parcial)**  
- Definir models iniciais: Produto, Usuário, Venda.  
- Configurar Alembic para migrations.  
- Sincronizar banco com schema inicial.  
➡️ Afeta: CRUDs, autenticação e vendas, pois dependem dos models e migrations.

**Etapa 3 — Backend básico (Produtos)**  
- Implementar CRUD de produtos.  
- Criar testes de inserção/listagem.  
- Validar documentação automática no Swagger.  
➡️ Afeta: testes de vendas (estoque), frontend futuro (listagem de produtos).

**Etapa 4 — Revisão Models + Seeds + Migrations**  
- Revisar models e relacionamentos.  
- Criar seeds para dados iniciais.  
- Aplicar migrations e validar subida do FastAPI sem erros.  
➡️ Afeta: consistência do banco, testes automatizados e dados iniciais para frontend.

**Etapa 5 — Autenticação e Autorização**  
- Implementar login/registro.  
- Configurar JWT e middleware de validação.  
- Restringir acesso por role.  
➡️ Afeta: rotas protegidas (produtos, usuários, vendas), testes de autorização, segurança geral.

**Etapa 6 — Vendas (CRUD)**  
- Consolidar rotas `/vendas` (listar, criar, atualizar, deletar).  
- Validar regras de negócio (estoque, cliente existente, vendedor autenticado).  
➡️ Afeta: fluxo principal da aplicação, base para relatórios e ETL.

**Etapa 7 — ETL e Validação de Dados**  
- Implementar rotas `/etl/import` e `/etl/export`.  
- Uso de **pandas** para tratamento e normalização.  
- Permitir que **admin** suba dados externos e extraia dados do banco.  
- Validar consistência geral das regras de negócio.  
- Criar testes de sucesso e erro cobrindo todos os cenários críticos.  
➡️ Afeta: integração com relatórios, análise de dados e estudo prático de pandas + BI.

---

### 🔜 Próximas Etapas

**Etapa 8 — Frontend inicial**  
- Criar telas em React (produtos, usuários, vendas).  
- Consumir APIs do backend.  
- Validar integração frontend ↔ backend.  
➡️ Afeta: experiência do usuário, validação prática das rotas.

**Etapa 9 — Mensageria**  
- Subir RabbitMQ no Docker Compose.  
- Publicar evento `VendaCriada`.  
- Criar consumidor simples para logar eventos.  
➡️ Afeta: escalabilidade, integração com outros serviços.

**Etapa 10 — Relatórios**  
- Integrar Metabase/Power BI ao banco.  
- Criar dashboards (vendas por região, receita por produto, desempenho de vendedores).  
➡️ Afeta: análise de negócio, tomada de decisão.

**Etapa 11 — Inteligência Artificial + CI/CD**  
- Criar endpoint `/recomendacoes`.  
- Treinar modelo simples com histórico de vendas.  
- Configurar pipeline CI/CD (GitHub Actions).  
- Deploy em nuvem (Render, Railway, Fly.io).  
➡️ Afeta: automação, inteligência de negócio, entrega contínua.

---

## ✅ Status atual
- CRUD de **Produtos, Usuários e Vendas** implementado e testado.  
- Autenticação e autorização com JWT funcionando.  
- ETL de vendas concluído (import/export com validações e testes).  
- Cobertura de testes sólida (~94%).  
- Estrutura pronta para avançar para **Etapa 8 — Frontend inicial**.  

---

## 🎯 Objetivo final
Ao término das etapas, o projeto será um **MVP funcional de loja online fullstack**, cobrindo:  
- Backend com FastAPI e banco MySQL.  
- Frontend em React.  
- Testes automatizados.  
- Mensageria e relatórios.  
- Deploy com CI/CD.  
- Extensível para estudos posteriores em segurança, mensageria, BI, IA e DevOps.  
