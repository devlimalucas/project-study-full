CREATE TABLE IF NOT EXISTS vendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Data DATE,
    Produto VARCHAR(100),
    Categoria VARCHAR(100),
    Cliente VARCHAR(100),
    Regiao VARCHAR(100),
    Quantidade INT,
    Preco_Unitario DECIMAL(10,2),
    Receita DECIMAL(10,2)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

LOAD DATA INFILE '/docker-entrypoint-initdb.d/vendas.csv'
INTO TABLE vendas
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Data, Produto, Categoria, Cliente, Regiao, Quantidade, Preco_Unitario, Receita);
