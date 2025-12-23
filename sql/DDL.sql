CREATE TABLE Pessoa (
	Cc VARCHAR(20) PRIMARY KEY,
	Nome VARCHAR(100) NOT NULL,
	Email varchar(100) UNIQUE NOT NULL,
	DataNascimento DATE NOT NULL,
	Morada VARCHAR(100) NOT NULL,
	NumTelefone VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE Empresa(
	Nif VARCHAR(20) PRIMARY KEY,
	Nome VARCHAR(100) UNIQUE NOT NULL,
	Localizacao VARCHAR(100) NOT NULL,
	NumTelefone VARCHAR(20) UNIQUE NOT NULL,
	Email varchar(100) UNIQUE NOT NULL
);

CREATE TABLE Distribuidora(
	Id INT IDENTITY(1,1) PRIMARY KEY,
	Nome VARCHAR(100) UNIQUE NOT NULL,
	Localizacao VARCHAR(100) NOT NULL,	
);

CREATE TABLE Armazem(
	Id INT IDENTITY(1,1) PRIMARY KEY,
	Localizacao VARCHAR(100) NOT NULL,	
	Capacidade INT NOT NULL
);

CREATE TABLE Cargo (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Nome VARCHAR(100) UNIQUE NOT NULL,
    Descricao VARCHAR(200)
);

CREATE TABLE Fabrica(
	Id INT IDENTITY(1,1) PRIMARY KEY,
    Nome VARCHAR(100) UNIQUE NOT NULL,
    Localizacao VARCHAR(100) NOT NULL,
    Empresa_Nif VARCHAR(20) NOT NULL,
    Distribuidora_Id INT NOT NULL,
    FOREIGN KEY (Empresa_Nif) REFERENCES Empresa(Nif),
    FOREIGN KEY (Distribuidora_Id) REFERENCES Distribuidora(Id)
);

CREATE TABLE Vendedor(
	Pessoa_Cc VARCHAR(20) PRIMARY KEY, 
    Id INT IDENTITY(1,1) UNIQUE NOT NULL,
    NumVendas INT NOT NULL,
    Cargo_Id INT NOT NULL,
    FOREIGN KEY (Pessoa_Cc) REFERENCES Pessoa(Cc),
    FOREIGN KEY (Cargo_Id) REFERENCES Cargo(Id)
);

CREATE TABLE Funcionario(
	Pessoa_Cc VARCHAR(20) PRIMARY KEY,
    Id INT IDENTITY(1,1) UNIQUE NOT NULL,
    Cargo_Id INT NOT NULL,
    Empresa_Nif VARCHAR(20) NOT NULL,
    Fabrica_Id INT,
    FOREIGN KEY (Pessoa_Cc) REFERENCES Pessoa(Cc),
    FOREIGN KEY (Cargo_Id) REFERENCES Cargo(Id),
    FOREIGN KEY (Empresa_Nif) REFERENCES Empresa(Nif),
    FOREIGN KEY (Fabrica_Id) REFERENCES Fabrica(Id)
);

CREATE TABLE Cliente(
	Pessoa_Cc VARCHAR(20) PRIMARY KEY,
    Nif VARCHAR(20) UNIQUE NOT NULL,
    FOREIGN KEY (Pessoa_Cc) REFERENCES Pessoa(Cc)
);

CREATE TABLE ContratoVendedor(
	DataIn DATE NOT NULL,
	DataOut DATE,
    Empresa_Nif VARCHAR(20) NOT NULL,
    Vendedor_Id INT NOT NULL,
    PRIMARY KEY (Empresa_Nif, Vendedor_Id),
    FOREIGN KEY (Empresa_Nif) REFERENCES Empresa(Nif),
    FOREIGN KEY (Vendedor_Id) REFERENCES Vendedor(Id)
);



CREATE TABLE Maquina(
	Id INT IDENTITY(1,1) PRIMARY KEY,
    Descricao VARCHAR(200) NOT NULL,
    Tipo VARCHAR(100) NOT NULL,
    Fabrica_Id INT NOT NULL,
    FOREIGN KEY (Fabrica_Id) REFERENCES Fabrica(Id)
);

CREATE TABLE Produto(
	Referencia VARCHAR(20) PRIMARY KEY,
    Descricao VARCHAR(200) NOT NULL,
    Nome VARCHAR(100) UNIQUE NOT NULL,
    Preco INT NOT NULL,
    Maquina_Id INT NOT NULL,
    Distribuidora_Id INT NOT NULL,
    FOREIGN KEY (Maquina_Id) REFERENCES Maquina(Id),
    FOREIGN KEY (Distribuidora_Id) REFERENCES Distribuidora(Id)
);

CREATE TABLE DistribuidoraArmazem(
	Distribuidora_Id INT NOT NULL,
    Armazem_Id INT NOT NULL,
    PRIMARY KEY (Distribuidora_Id, Armazem_Id),
    FOREIGN KEY (Distribuidora_Id) REFERENCES Distribuidora(Id),
    FOREIGN KEY(Armazem_Id) REFERENCES Armazem(Id)
); 

CREATE TABLE Stock(
    UltimoMov DATE NOT NULL,
    Quantidade INT NOT NULL,
    Produto_Referencia VARCHAR(20) NOT NULL,
    Armazem_Id INT NOT NULL,
    PRIMARY KEY (Produto_Referencia, Armazem_Id),
    FOREIGN KEY(Produto_Referencia) REFERENCES Produto(Referencia),
    FOREIGN KEY(Armazem_Id) REFERENCES Armazem(Id)
);

CREATE TABLE Fornecedor(
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Nome VARCHAR(100) UNIQUE NOT NULL,
    Empresa_Nif VARCHAR(20) NOT NULL,
    FOREIGN KEY (Empresa_Nif) REFERENCES Empresa(Nif)
);

CREATE TABLE MateriaPrima(
    Referencia VARCHAR(20) PRIMARY KEY,
    Descricao VARCHAR(200) NOT NULL,
    Fornecedor_Id INT NOT NULL,
    FOREIGN KEY(Fornecedor_Id) REFERENCES Fornecedor(Id)
);

CREATE TABLE Loja(
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Localizacao VARCHAR(100) NOT NULL,    
    Armazem_Id INT NOT NULL,
    FOREIGN KEY(Armazem_Id) REFERENCES Armazem(Id)
);

CREATE TABLE Venda(
    Id INT IDENTITY(1,1) PRIMARY KEY,
    DataHora DATE NOT NULL,
    ValorTotal INT NOT NULL,
    MetodoPagamento VARCHAR(100) NOT NULL,
    Loja_Id INT NOT NULL,
    Cliente_Pessoa_Cc VARCHAR(20) NOT NULL,
    FOREIGN KEY(Loja_Id) REFERENCES Loja(Id),
    FOREIGN KEY(Cliente_Pessoa_Cc) REFERENCES Cliente(Pessoa_Cc)
);

CREATE TABLE Item(
    Quantidade INT NOT NULL,
    Preco DECIMAL(10, 2) NOT NULL,
    Venda_Id INT NOT NULL,
    Produto_Referencia VARCHAR(20) NOT NULL,
    PRIMARY KEY (Venda_Id, Produto_Referencia),
    FOREIGN KEY(Venda_Id) REFERENCES Venda(Id),
    FOREIGN KEY(Produto_Referencia) REFERENCES Produto(Referencia)
);