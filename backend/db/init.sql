CREATE DATABASE IF NOT EXISTS kanastra;
USE kanastra;

-- Suas tabelas e dados iniciais
CREATE TABLE IF NOT EXISTS debts (
                                     id INT AUTO_INCREMENT PRIMARY KEY,
                                     name VARCHAR(255) NOT NULL,
    government_id VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    debt_amount DECIMAL(10, 2) NOT NULL,
    debt_due_date DATE NOT NULL,
    debt_id VARCHAR(255) NOT NULL
    );

-- Adicione mais tabelas e dados iniciais conforme necessário
