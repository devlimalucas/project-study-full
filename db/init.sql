-- init.sql correto: apenas configuração inicial do banco

-- Garante que o banco use UTF-8 completo
ALTER DATABASE loja CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Opcional: define charset padrão para novas tabelas
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET collation_connection = utf8mb4_unicode_ci;

-- Se quiser criar um usuário específico para a aplicação:
-- CREATE USER 'appuser'@'%' IDENTIFIED BY 'senha_segura';
-- GRANT ALL PRIVILEGES ON loja.* TO 'appuser'@'%';
-- FLUSH PRIVILEGES;

