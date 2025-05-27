# **Sistema de Controle de Estacionamento** 🚗

## **Objetivo** 🎯

Desenvolver um sistema de controle de estacionamento para gerenciar os dados dos clientes e veículos de forma eficiente. O sistema permitirá o cadastro, alteração, exclusão e consulta de clientes e seus respectivos veículos. 💻

## **Problema** ❌

Estacionamentos frequentemente enfrentam dificuldades na gestão de clientes e veículos, como a falta de organização e o controle manual ineficiente. Sem um sistema adequado, os registros podem se perder ou ficar desorganizados, prejudicando a operação.

## **Solução** ✅

Este sistema digitalizará o processo de gerenciamento de estacionamento, criando um banco de dados de clientes e veículos, acessível via interface de usuário, permitindo registrar, alterar, excluir e consultar informações rapidamente. 🚗📱

## **Tecnologias** 💻

O projeto será desenvolvido utilizando as seguintes tecnologias:

* **Python** para a lógica do sistema
* **MySQL** para o banco de dados


## **Banco de Dados** 💾

O banco de dados será estruturado da seguinte forma:

### **Tabelas:**

1. **Clientes**

   * **ID\_cliente** (PK)
   * **Nome** (VARCHAR)
   * **Endereço** (VARCHAR)
   * **CPF** (VARCHAR, único)
   * **Telefone** (VARCHAR)

2. **Veículos**

   * **ID\_veículo** (PK)
   * **ID\_cliente** (FK - relaciona com a tabela de clientes)
   * **Marca** (VARCHAR)
   * **Modelo** (VARCHAR)
   * **Ano** (INT)
   * **Placa** (VARCHAR, único)

### **Relacionamento:**

* **1 Cliente pode ter múltiplos veículos** — relacionamento de **1\:N** entre **Clientes** e **Veículos**.

## **Requisitos Funcionais** ✅

1. **Cadastro de Clientes**
   O sistema deverá permitir que um cliente seja cadastrado com os seguintes dados: Nome, Endereço, CPF e Telefone.

2. **Cadastro de Veículos**
   O sistema deverá permitir que o veículo de um cliente seja cadastrado com os seguintes dados: Marca, Modelo, Ano, Placa.

3. **Alteração de Dados**
   O sistema deverá permitir a alteração dos dados de um cliente (Nome, Endereço, Telefone) ou de um veículo (Marca, Modelo, Ano, Placa).

4. **Exclusão de Registros**
   O sistema deverá permitir a exclusão de um cliente ou de um veículo de forma eficiente.

5. **Consulta de Registros**
   O sistema deverá permitir a consulta de registros tanto de clientes quanto de veículos cadastrados.

## **Requisitos Não Funcionais** ✅

* **Performance**: O sistema deve ser capaz de processar operações de cadastro, atualização, exclusão e consulta rapidamente, mesmo com um grande número de registros.
* **Segurança**: O sistema deverá garantir que os dados de CPF e placas dos veículos sejam manipulados de forma segura.
* **Facilidade de Uso**: A interface do usuário deve ser intuitiva, seja em linha de comando ou com interface gráfica, permitindo fácil navegação.

## **Equipe** 👥

O projeto será desenvolvido por \[Nome do Desenvolvedor] (coloque seu nome aqui). Em caso de colaboração, adicionar nomes de outros membros.

## **Benefícios** 🌟

### **Clientes** 🎓

* **Organização:** O sistema trará mais organização para os registros de clientes e veículos, facilitando o controle de acesso.
* **Segurança e Eficiência:** Dados dos clientes e veículos estarão acessíveis rapidamente e de maneira segura.

### **Funcionários do Estacionamento** 👨‍💼

* **Facilidade no Controle:** A operação do estacionamento será mais eficiente com o sistema, permitindo fácil cadastro, alteração e consulta de registros.
* **Controle Total:** O sistema proporcionará um controle completo sobre a disponibilidade e histórico dos veículos.

## **Próximos Passos** 🚀

1. **Definição do Banco de Dados:** Criar as tabelas no MySQL e estabelecer o relacionamento entre as entidades (clientes e veículos).
2. **Desenvolvimento do Backend:** Implementar a lógica de cadastro, alteração, exclusão e consulta utilizando Python e integração com o banco de dados MySQL.
3. **Testes do Sistema:** Testar o sistema para garantir que todas as operações estão funcionando conforme esperado.
4. **Documentação e Implantação:** Documentar o código e implantar o sistema.

## **Impacto Esperado** 🌍

O Sistema de Controle de Estacionamento ajudará a otimizar a gestão dos veículos e clientes, reduzindo erros e aumentando a produtividade dos funcionários. 🏢

## **Métricas de Sucesso** 📊

O sucesso do projeto será medido por meio das seguintes métricas:

* **Número de registros de clientes cadastrados**
* **Número de registros de veículos cadastrados**
* **Quantidade de operações de consulta realizadas**
* **Quantidade de operações de exclusão ou alteração de registros**

## **Estrutura de Banco de Dados** 💾

### **SQL para Criação das Tabelas:**

```sql
CREATE DATABASE Estacionamento;

USE Estacionamento;

-- Tabela de Clientes
CREATE TABLE Clientes (
    ID_cliente INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Endereco VARCHAR(200),
    CPF VARCHAR(11) UNIQUE NOT NULL,
    Telefone VARCHAR(15)
);

-- Tabela de Veículos
CREATE TABLE Veiculos (
    ID_veiculo INT AUTO_INCREMENT PRIMARY KEY,
    ID_cliente INT,
    Marca VARCHAR(50),
    Modelo VARCHAR(50),
    Ano INT,
    Placa VARCHAR(7) UNIQUE NOT NULL,
    FOREIGN KEY (ID_cliente) REFERENCES Clientes(ID_cliente)
);
```

## **Conclusão** 🎉

O **Sistema de Controle de Estacionamento** é uma ferramenta poderosa para otimizar a gestão de veículos e clientes. A utilização de Python para a lógica do sistema e MySQL para o armazenamento de dados garante uma solução robusta e eficiente. 🏅
