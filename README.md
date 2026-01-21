# 🛒 Loja Online

Projeto **fullstack** de uma loja online, desenvolvido com **FastAPI** no backend e **React + Vite + TypeScript** no frontend.  
Banco de dados: **MySQL via Docker**.  

🎯 **Objetivo**: praticar boas práticas de desenvolvimento, testes automatizados e deploy com CI/CD, explorando o ciclo completo de um app moderno.

---

## 🚀 Tecnologias

- **Backend**: FastAPI + SQLAlchemy  
- **Frontend**: React + Vite + TypeScript  
- **Banco**: MySQL (Docker)  
- **Testes**: Pytest (backend), Jest + React Testing Library (frontend)  
- **Deploy**: Docker Compose  

---

## 📆 Plano de Estudos (11 Dias)

### ✅ Concluído
- **Dia 1 — Infraestrutura**  
  - Configuração do Docker Compose com MySQL + FastAPI + React.  
  - Containers comunicando em rede.  
  - Banco inicializado com charset correto.  

- **Dia 2 — Modelos e Banco (parcial)**  
  - Criados models iniciais: Produto, Usuário, Venda.  
  - Migrations rodando com Alembic.  
  - Banco sincronizado com os models.  
  - Ajuste posterior: `Usuario` passou a ter `senha_hash` e `role`.  

- **Dia 3 — Backend básico (Produtos)**  
  - CRUD de produtos implementado.  
  - Testes de inserção e listagem funcionando.  
  - Documentação via Swagger disponível.  

- **Dia 4 — Revisão Models + Seeds + Migrations + CRUD completo**  
  - Models revisados e alinhados com o banco.  
  - Seeds rodando (produtos e usuários iniciais).  
  - Migration inicial aplicada com sucesso.  
  - FastAPI sobe sem erro.  
  - CRUD completo de **Produtos, Usuários e Vendas** implementado.  
  - Testes automatizados cobrindo criação, listagem, obtenção, atualização e exclusão.  
  - Testes de erros para cenários como estoque insuficiente e entidades inexistentes.  
  - Estrutura de testes reorganizada em módulos (`produtos/`, `usuarios/`, `vendas/`) com uso de factories.  
  - Atualizado `requirements.txt` para incluir `email-validator`.  

---

### 🔜 Próximos passos
- **Dia 5 — Autenticação e Autorização**  
  - Implementar login/registro de usuários.  
  - Configurar JWT para proteger rotas.  
  - Middleware de validação de token.  
  - Restringir rotas por role (admin, cliente, vendedor).  

- **Dia 6 — Vendas (refino)**  
  - Importação de vendas via CSV.  
  - Validações extras (quantidade inválida, data inválida).  

- **Dia 7 — ETL**  
  - Pipeline para importar/exportar dados (CSV ↔ banco).  
  - Normalização de dados externos.  
  - Automatizar carga de vendas/produtos.  

- **Dia 8 — Frontend inicial**  
  - Criar telas em React (produtos, usuários, vendas).  
  - Consumir APIs do backend.  
  - Validar integração frontend ↔ backend.  

- **Dia 9 — Mensageria**  
  - Subir RabbitMQ no Docker Compose.  
  - Publicar evento `VendaCriada`.  
  - Criar consumidor simples para logar eventos.  

- **Dia 10 — Relatórios**  
  - Integrar Metabase/Power BI ao banco.  
  - Criar dashboards (vendas por região, receita por produto, desempenho de vendedores).  

- **Dia 11 — Inteligência Artificial + CI/CD**  
  - Criar endpoint `/recomendacoes`.  
  - Treinar modelo simples com histórico de vendas.  
  - Configurar pipeline CI/CD (GitHub Actions).  
  - Deploy em nuvem (Render, Railway, Fly.io).  

---

## ✅ Status atual
- CRUD de **Produtos, Usuários e Vendas** implementado e testado.  
- Cobertura de testes sólida (~92%).  
- Estrutura pronta para avançar para autenticação (Dia 5).  

---

## 🎯 Objetivo final
Ao término dos 11 dias, o projeto será um **MVP funcional de loja online fullstack**, cobrindo:  
- Backend com FastAPI e banco MySQL.  
- Frontend em React.  
- Testes automatizados.  
- Mensageria e relatórios.  
- Deploy com CI/CD.  
- Extensível para estudos posteriores em segurança, mensageria, BI, IA e DevOps.  

