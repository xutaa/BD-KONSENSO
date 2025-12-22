-- =============================================
-- STORED PROCEDURES DE ATUALIZAÇÃO - BD-KONSENSO
-- Executa este ficheiro no SSMS para criar todos os SPs
-- =============================================

USE p2g4;
GO

-- =============================================
-- SP: AtualizarCliente
-- =============================================
CREATE OR ALTER PROCEDURE dbo.AtualizarCliente
    @Pessoa_Cc VARCHAR(20),
    @Nome VARCHAR(100),
    @Email VARCHAR(100),
    @DataNascimento DATE,
    @Morada VARCHAR(200),
    @NumTelefone VARCHAR(20),
    @Nif VARCHAR(9)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Atualizar dados na tabela Pessoa
        UPDATE dbo.Pessoa
        SET Nome = @Nome, Email = @Email, DataNascimento = @DataNascimento, 
            Morada = @Morada, NumTelefone = @NumTelefone
        WHERE Cc = @Pessoa_Cc;
        
        -- Atualizar NIF na tabela Cliente
        UPDATE dbo.Cliente
        SET Nif = @Nif
        WHERE Pessoa_Cc = @Pessoa_Cc;
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- =============================================
-- SP: AtualizarFuncionario
-- =============================================
CREATE OR ALTER PROCEDURE dbo.AtualizarFuncionario
    @Pessoa_Cc VARCHAR(20),
    @Nome VARCHAR(100),
    @Email VARCHAR(100),
    @DataNascimento DATE,
    @Morada VARCHAR(200),
    @NumTelefone VARCHAR(20),
    @Cargo_Id INT,
    @Empresa_Nif VARCHAR(9),
    @Fabrica_Id INT = NULL
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        UPDATE dbo.Pessoa
        SET Nome = @Nome, Email = @Email, DataNascimento = @DataNascimento, 
            Morada = @Morada, NumTelefone = @NumTelefone
        WHERE Cc = @Pessoa_Cc;
        
        UPDATE dbo.Funcionario
        SET Cargo_Id = @Cargo_Id, Empresa_Nif = @Empresa_Nif, Fabrica_Id = @Fabrica_Id
        WHERE Pessoa_Cc = @Pessoa_Cc;
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- =============================================
-- SP: AtualizarVendedor
-- =============================================
CREATE OR ALTER PROCEDURE dbo.AtualizarVendedor
    @Pessoa_Cc VARCHAR(20),
    @Nome VARCHAR(100),
    @Email VARCHAR(100),
    @DataNascimento DATE,
    @Morada VARCHAR(200),
    @NumTelefone VARCHAR(20),
    @Cargo_Id INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        UPDATE dbo.Pessoa
        SET Nome = @Nome, Email = @Email, DataNascimento = @DataNascimento, 
            Morada = @Morada, NumTelefone = @NumTelefone
        WHERE Cc = @Pessoa_Cc;
        
        UPDATE dbo.Vendedor
        SET Cargo_Id = @Cargo_Id
        WHERE Pessoa_Cc = @Pessoa_Cc;
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- =============================================
-- SP: AtualizarCargo
-- =============================================
CREATE OR ALTER PROCEDURE dbo.AtualizarCargo
    @Id INT,
    @Nome VARCHAR(100),
    @Descricao VARCHAR(200)
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.Cargo
    SET Nome = @Nome, Descricao = @Descricao
    WHERE Id = @Id;
END
GO

-- =============================================
-- SP: AtualizarEmpresa
-- =============================================
CREATE OR ALTER PROCEDURE dbo.AtualizarEmpresa
    @Nif VARCHAR(9),
    @Nome VARCHAR(100),
    @Localizacao VARCHAR(100),
    @NumTelefone VARCHAR(20),
    @Email VARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.Empresa
    SET Nome = @Nome, Localizacao = @Localizacao, 
        NumTelefone = @NumTelefone, Email = @Email
    WHERE Nif = @Nif;
END
GO

-- =============================================
-- SP: AtualizarFornecedor
-- =============================================
CREATE OR ALTER PROCEDURE dbo.AtualizarFornecedor
    @Id INT,
    @Nome VARCHAR(100),
    @Empresa_Nif VARCHAR(9)
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.Fornecedor
    SET Nome = @Nome, Empresa_Nif = @Empresa_Nif
    WHERE Id = @Id;
END
GO

-- =============================================
-- SP: AtualizarDistribuidora
-- =============================================
CREATE OR ALTER PROCEDURE dbo.AtualizarDistribuidora
    @Id INT,
    @Nome VARCHAR(100),
    @Localizacao VARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.Distribuidora
    SET Nome = @Nome, Localizacao = @Localizacao
    WHERE Id = @Id;
END
GO

-- =============================================
-- SP: AtualizarArmazem
-- =============================================
CREATE OR ALTER PROCEDURE dbo.AtualizarArmazem
    @Id INT,
    @Localizacao VARCHAR(100),
    @Capacidade INT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.Armazem
    SET Localizacao = @Localizacao, Capacidade = @Capacidade
    WHERE Id = @Id;
END
GO

-- =============================================
-- SP: AtualizarLoja
-- =============================================
CREATE OR ALTER PROCEDURE dbo.AtualizarLoja
    @Id INT,
    @Nome VARCHAR(100),
    @Localizacao VARCHAR(100),
    @Armazem_Id INT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.Loja
    SET Nome = @Nome, Localizacao = @Localizacao, Armazem_Id = @Armazem_Id
    WHERE Id = @Id;
END
GO

-- =============================================
-- SP: AtualizarFabrica
-- =============================================
CREATE OR ALTER PROCEDURE dbo.AtualizarFabrica
    @Id INT,
    @Nome VARCHAR(100),
    @Localizacao VARCHAR(100),
    @Empresa_Nif VARCHAR(9),
    @Distribuidora_Id INT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.Fabrica
    SET Nome = @Nome, Localizacao = @Localizacao, 
        Empresa_Nif = @Empresa_Nif, Distribuidora_Id = @Distribuidora_Id
    WHERE Id = @Id;
END
GO

-- =============================================
-- SP: AtualizarMaquina
-- =============================================
CREATE OR ALTER PROCEDURE dbo.AtualizarMaquina
    @Id INT,
    @Descricao VARCHAR(200),
    @Tipo VARCHAR(50),
    @Fabrica_Id INT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.Maquina
    SET Descricao = @Descricao, Tipo = @Tipo, Fabrica_Id = @Fabrica_Id
    WHERE Id = @Id;
END
GO

-- =============================================
-- SP: AtualizarMateriaPrima
-- =============================================
CREATE OR ALTER PROCEDURE dbo.AtualizarMateriaPrima
    @Referencia VARCHAR(20),
    @Descricao VARCHAR(200),
    @Fornecedor_Id INT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.MateriaPrima
    SET Descricao = @Descricao, Fornecedor_Id = @Fornecedor_Id
    WHERE Referencia = @Referencia;
END
GO

-- =============================================
-- SP: AtualizarStock
-- =============================================
CREATE OR ALTER PROCEDURE dbo.AtualizarStock
    @Produto_Referencia VARCHAR(20),
    @Armazem_Id INT,
    @Quantidade INT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.Stock
    SET Quantidade = @Quantidade, UltimoMov = GETDATE()
    WHERE Produto_Referencia = @Produto_Referencia AND Armazem_Id = @Armazem_Id;
END
GO

-- =============================================
-- SP: AtualizarContratoVendedor
-- =============================================
CREATE OR ALTER PROCEDURE dbo.AtualizarContratoVendedor
    @Vendedor_Id INT,
    @Empresa_Nif VARCHAR(20),
    @DataIn DATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.ContratoVendedor
    SET DataIn = @DataIn
    WHERE Vendedor_Id = @Vendedor_Id AND Empresa_Nif = @Empresa_Nif;
END
GO

PRINT '✅ Todos os 14 Stored Procedures de Atualização criados com sucesso!';
GO
