CREATE DATABASE IF NOT EXISTS estacionamento_db;
USE estacionamento_db;
CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,  
    nome VARCHAR(255) NOT NULL,         
    endereco VARCHAR(255),              
    cpf VARCHAR(11) NOT NULL UNIQUE,    
    telefone VARCHAR(20)               
);


CREATE TABLE IF NOT EXISTS veiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,      
    marca VARCHAR(100) NOT NULL,           
    modelo VARCHAR(100) NOT NULL,           
    ano INT,                                
    placa VARCHAR(8) NOT NULL UNIQUE,       
    cliente_id INT NOT NULL,                
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) 
        ON DELETE CASCADE                 
        ON UPDATE CASCADE                  
);


CREATE INDEX idx_cpf ON clientes(cpf);              
CREATE INDEX idx_placa ON veiculos(placa);          
CREATE INDEX idx_cliente_id ON veiculos(cliente_id);