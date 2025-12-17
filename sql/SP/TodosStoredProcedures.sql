-- =============================================
-- STORED PROCEDURES - BD-KONSENSO
-- Consolidação de todos os SPs do sistema
-- Data: 17/12/2025
-- =============================================

-- =============================================
-- SP: InserirNovaEmpresa
-- Descrição: Insere uma nova empresa no sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovaEmpresa
    @Nif VARCHAR(20),
    @Nome VARCHAR(100),
    @Localizacao VARCHAR(200),
    @NumTelefone VARCHAR(20),
    @Email VARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        IF LTRIM(RTRIM(@Nif)) = '' OR LTRIM(RTRIM(@Nome)) = ''
        BEGIN
            RAISERROR('NIF e Nome são obrigatórios.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Empresa WHERE Nif = @Nif)
        BEGIN
            RAISERROR('Já existe uma empresa com este NIF.', 16, 1);
            RETURN;
        END
        
        IF @Email IS NOT NULL AND @Email NOT LIKE '%_@__%.__%'
        BEGIN
            RAISERROR('Email inválido.', 16, 1);
            RETURN;
        END
        
        INSERT INTO dbo.Empresa (Nif, Nome, Localizacao, NumTelefone, Email)
        VALUES (@Nif, @Nome, @Localizacao, @NumTelefone, @Email);
        
        PRINT 'Empresa inserida com sucesso!';
        
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO

-- =============================================
-- SP: InserirNovaFabrica
-- Descrição: Insere uma nova fábrica no sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovaFabrica
    @Nome VARCHAR(100),
    @Localizacao VARCHAR(200),
    @EmpresaNif VARCHAR(20),
    @DistribuidoraId INT
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        IF LTRIM(RTRIM(@Nome)) = '' OR LTRIM(RTRIM(@Localizacao)) = ''
        BEGIN
            RAISERROR('Nome e Localização são obrigatórios.', 16, 1);
            RETURN;
        END
        
        IF NOT EXISTS (SELECT 1 FROM dbo.Empresa WHERE Nif = @EmpresaNif)
        BEGIN
            RAISERROR('Empresa não existe.', 16, 1);
            RETURN;
        END
        
        IF NOT EXISTS (SELECT 1 FROM dbo.Distribuidora WHERE Id = @DistribuidoraId)
        BEGIN
            RAISERROR('Distribuidora não existe.', 16, 1);
            RETURN;
        END
        
        INSERT INTO dbo.Fabrica (Nome, Localizacao, Empresa_Nif, Distribuidora_Id)
        VALUES (@Nome, @Localizacao, @EmpresaNif, @DistribuidoraId);
        
        PRINT 'Fábrica inserida com sucesso!';
        
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO

-- =============================================
-- SP: InserirNovaMaquina
-- Descrição: Insere uma nova máquina no sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovaMaquina
    @Descricao VARCHAR(200),
    @Tipo VARCHAR(50),
    @FabricaId INT
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        IF LTRIM(RTRIM(@Descricao)) = '' OR LTRIM(RTRIM(@Tipo)) = ''
        BEGIN
            RAISERROR('Descrição e Tipo são obrigatórios.', 16, 1);
            RETURN;
        END
        
        IF NOT EXISTS (SELECT 1 FROM dbo.Fabrica WHERE Id = @FabricaId)
        BEGIN
            RAISERROR('Fábrica não existe.', 16, 1);
            RETURN;
        END
        
        INSERT INTO dbo.Maquina (Descricao, Tipo, Fabrica_Id)
        VALUES (@Descricao, @Tipo, @FabricaId);
        
        PRINT 'Máquina inserida com sucesso!';
        
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO

-- =============================================
-- SP: InserirNovaMateriaPrima
-- Descrição: Insere uma nova matéria-prima no sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovaMateriaPrima
    @Referencia VARCHAR(20),
    @Descricao VARCHAR(200),
    @FornecedorId INT
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        IF EXISTS (SELECT 1 FROM dbo.MateriaPrima WHERE Referencia = @Referencia)
        BEGIN
            RAISERROR('Referência já existe no sistema.', 16, 1)
            RETURN
        END

        IF NOT EXISTS (SELECT 1 FROM dbo.Fornecedor WHERE Id = @FornecedorId)
        BEGIN
            RAISERROR('Fornecedor não encontrado.', 16, 1)
            RETURN
        END

        INSERT INTO dbo.MateriaPrima (Referencia, Descricao, Fornecedor_Id)
        VALUES (@Referencia, @Descricao, @FornecedorId);
        
        SELECT @Referencia AS Referencia, 'INSERIDO' AS Acao;
    END TRY
    BEGIN CATCH
        THROW;
        RETURN;
    END CATCH
END
GO

-- =============================================
-- SP: InserirNovoArmazem
-- Descrição: Insere um novo armazém no sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovoArmazem
    @Localizacao VARCHAR(200),
    @Capacidade INT
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        IF LTRIM(RTRIM(@Localizacao)) = ''
        BEGIN
            RAISERROR('Localização é obrigatória.', 16, 1);
            RETURN;
        END
        
        IF @Capacidade <= 0
        BEGIN
            RAISERROR('Capacidade deve ser maior que zero.', 16, 1);
            RETURN;
        END
        
        INSERT INTO dbo.Armazem (Localizacao, Capacidade)
        VALUES (@Localizacao, @Capacidade);
        
        PRINT 'Armazém inserido com sucesso!';
        
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO

-- =============================================
-- SP: InserirNovoCargo
-- Descrição: Insere um novo cargo no sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovoCargo
    @Nome VARCHAR(100),
    @Descricao VARCHAR(200) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        IF LTRIM(RTRIM(@Nome)) = ''
        BEGIN
            RAISERROR('O nome do cargo não pode estar vazio.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Cargo WHERE Nome = @Nome)
        BEGIN
            RAISERROR('Já existe um cargo com este nome.', 16, 1);
            RETURN;
        END
        
        INSERT INTO dbo.Cargo (Nome, Descricao)
        VALUES (@Nome, @Descricao);
        
        PRINT 'Cargo inserido com sucesso!';
        
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO

-- =============================================
-- SP: InserirNovoCliente
-- Descrição: Insere um novo cliente no sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovoCliente
    @PessoaCc VARCHAR(20),
    @Nif VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Pessoa WHERE Cc = @PessoaCc)
        BEGIN
            RAISERROR('Pessoa não encontrada.', 16, 1)
            RETURN
        END

        IF EXISTS (SELECT 1 FROM dbo.Cliente WHERE Pessoa_Cc = @PessoaCc)
        BEGIN
            RAISERROR('Esta pessoa já está registada como cliente.', 16, 1)
            RETURN
        END

        IF EXISTS (SELECT 1 FROM dbo.Cliente WHERE Nif = @Nif)
        BEGIN
            RAISERROR('NIF já existe no sistema.', 16, 1)
            RETURN
        END

        INSERT INTO dbo.Cliente (Pessoa_Cc, Nif)
        VALUES (@PessoaCc, @Nif);
        
        SELECT @PessoaCc AS PessoaCc, 'INSERIDO' AS Acao;
    END TRY
    BEGIN CATCH
        THROW;
        RETURN;
    END CATCH
END
GO

-- =============================================
-- SP: InserirNovoContratoVendedor
-- Descrição: Insere um novo contrato de vendedor
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovoContratoVendedor
    @VendedorId INT,
    @EmpresaNif VARCHAR(20),
    @DataIn DATE
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Vendedor WHERE Id = @VendedorId)
        BEGIN
            RAISERROR('Vendedor não existe.', 16, 1);
            RETURN;
        END
        
        IF NOT EXISTS (SELECT 1 FROM dbo.Empresa WHERE Nif = @EmpresaNif)
        BEGIN
            RAISERROR('Empresa não existe.', 16, 1);
            RETURN;
        END
        
        IF @DataIn > GETDATE()
        BEGIN
            RAISERROR('A data de início não pode ser futura.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (
            SELECT 1 
            FROM dbo.ContratoVendedor 
            WHERE Vendedor_Id = @VendedorId 
              AND Empresa_Nif = @EmpresaNif
        )
        BEGIN
            RAISERROR('Já existe um contrato para este vendedor nesta empresa.', 16, 1);
            RETURN;
        END
        
        INSERT INTO dbo.ContratoVendedor (DataIn, Empresa_Nif, Vendedor_Id)
        VALUES (@DataIn, @EmpresaNif, @VendedorId);
        
        PRINT 'Contrato de vendedor inserido com sucesso!';
        
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO

-- =============================================
-- SP: InserirNovoFornecedor
-- Descrição: Insere um novo fornecedor no sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovoFornecedor
    @Nome VARCHAR(100),
    @EmpresaNif VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Empresa WHERE Nif = @EmpresaNif)
        BEGIN
            RAISERROR('Empresa não encontrada.', 16, 1)
            RETURN
        END

        IF EXISTS (SELECT 1 FROM dbo.Fornecedor WHERE Nome = @Nome)
        BEGIN
            RAISERROR('Já existe um fornecedor com este nome.', 16, 1)
            RETURN
        END

        INSERT INTO dbo.Fornecedor (Nome, Empresa_Nif)
        VALUES (@Nome, @EmpresaNif);
        
        SELECT SCOPE_IDENTITY() AS FornecedorId, 'INSERIDO' AS Acao;
    END TRY
    BEGIN CATCH
        THROW;
        RETURN;
    END CATCH
END
GO

-- =============================================
-- SP: InserirNovoFuncionario
-- Descrição: Insere um novo funcionário no sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovoFuncionario
    @PessoaCc VARCHAR(20),
    @CargoId INT,
    @EmpresaNif VARCHAR(20),
    @FabricaId INT = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Pessoa WHERE Cc = @PessoaCc)
        BEGIN
            RAISERROR('Pessoa com este CC não existe.', 16, 1);
            RETURN;
        END
        
        IF NOT EXISTS (SELECT 1 FROM dbo.Cargo WHERE Id = @CargoId)
        BEGIN
            RAISERROR('Cargo não existe.', 16, 1);
            RETURN;
        END
        
        IF NOT EXISTS (SELECT 1 FROM dbo.Empresa WHERE Nif = @EmpresaNif)
        BEGIN
            RAISERROR('Empresa não existe.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Funcionario WHERE Pessoa_Cc = @PessoaCc)
        BEGIN
            RAISERROR('Esta pessoa já é um funcionário.', 16, 1);
            RETURN;
        END
        
        IF @FabricaId IS NOT NULL AND NOT EXISTS (SELECT 1 FROM dbo.Fabrica WHERE Id = @FabricaId)
        BEGIN
            RAISERROR('Fábrica não existe.', 16, 1);
            RETURN;
        END
        
        INSERT INTO dbo.Funcionario (Pessoa_Cc, Cargo_Id, Empresa_Nif, Fabrica_Id)
        VALUES (@PessoaCc, @CargoId, @EmpresaNif, @FabricaId);
        
        PRINT 'Funcionário inserido com sucesso!';
        
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO

-- =============================================
-- SP: InserirNovoItem
-- Descrição: Insere um novo item numa venda
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovoItem
    @VendaId INT,
    @ProdutoReferencia VARCHAR(20),
    @Quantidade INT,
    @Preco DECIMAL(10, 2)
AS
BEGIN
    SET NOCOUNT ON;

    IF @Quantidade <= 0
    BEGIN
        RAISERROR('A quantidade deve ser maior que zero.', 16, 1)
        RETURN
    END

    IF @Preco <= 0
    BEGIN
        RAISERROR('O preço deve ser maior que zero.', 16, 1)
        RETURN
    END

    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Venda WHERE Id = @VendaId)
        BEGIN
            RAISERROR('Venda não encontrada.', 16, 1)
            RETURN
        END

        IF NOT EXISTS (SELECT 1 FROM dbo.Produto WHERE Referencia = @ProdutoReferencia)
        BEGIN
            RAISERROR('Produto não encontrado.', 16, 1)
            RETURN
        END

        IF EXISTS (SELECT 1 FROM dbo.Item WHERE Venda_Id = @VendaId AND Produto_Referencia = @ProdutoReferencia)
        BEGIN
            RAISERROR('Este produto já foi adicionado a esta venda.', 16, 1)
            RETURN
        END

        INSERT INTO dbo.Item (Venda_Id, Produto_Referencia, Quantidade, Preco)
        VALUES (@VendaId, @ProdutoReferencia, @Quantidade, @Preco);
        
        SELECT @VendaId AS VendaId, @ProdutoReferencia AS Referencia, 'INSERIDO' AS Acao;
    END TRY
    BEGIN CATCH
        THROW;
        RETURN;
    END CATCH
END
GO

-- =============================================
-- SP: InserirNovoProduto
-- Descrição: Insere um novo produto no sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovoProduto
    @Referencia VARCHAR(20),
    @Descricao VARCHAR(200),
    @NomeProduto VARCHAR(100),
    @Preco DECIMAL(10, 2),
    @MaquinaID INT,
    @DistribuidoraID INT
AS
BEGIN
    SET NOCOUNT ON;

    IF @Preco <= 0.00
    BEGIN
        RAISERROR('O preço deve ser um valor positivo.', 16, 1) 
        RETURN
    END

    BEGIN TRY
        INSERT INTO dbo.Produto (Referencia, Descricao, NomeProduto, Preco, MaquinaID, DistribuidoraID)
        VALUES (@Referencia, @Descricao, @NomeProduto, @Preco, @MaquinaID, @DistribuidoraID);
        SELECT SCOPE_IDENTITY() AS ProdutoID; 
    END TRY
    BEGIN CATCH
        THROW;
        RETURN;
    END CATCH
END
GO

-- =============================================
-- SP: InserirNovoStock
-- Descrição: Insere ou atualiza o stock de um produto
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovoStock
    @ProdutoReferencia VARCHAR(20),
    @ArmazemID INT,
    @Quantidade INT
AS
BEGIN
    SET NOCOUNT ON;

    IF @Quantidade <= 0
    BEGIN
        RAISERROR('A quantidade deve ser maior que zero.', 16, 1)
        RETURN
    END

    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Produto WHERE Referencia = @ProdutoReferencia)
        BEGIN
            RAISERROR('Produto não encontrado.', 16, 1)
            RETURN
        END

        IF NOT EXISTS (SELECT 1 FROM dbo.Armazem WHERE Id = @ArmazemID)
        BEGIN
            RAISERROR('Armazém não encontrado.', 16, 1)
            RETURN
        END

        IF EXISTS (SELECT 1 FROM dbo.Stock WHERE Produto_Referencia = @ProdutoReferencia AND Armazem_Id = @ArmazemID)
        BEGIN
            UPDATE dbo.Stock 
            SET Quantidade = Quantidade + @Quantidade,
                UltimoMov = GETDATE()
            WHERE Produto_Referencia = @ProdutoReferencia AND Armazem_Id = @ArmazemID;
            
            SELECT @ProdutoReferencia AS Referencia, @ArmazemID AS ArmazemID, 'ATUALIZADO' AS Acao;
        END
        ELSE
        BEGIN
            INSERT INTO dbo.Stock (Produto_Referencia, Armazem_Id, Quantidade, UltimoMov)
            VALUES (@ProdutoReferencia, @ArmazemID, @Quantidade, GETDATE());
            
            SELECT @ProdutoReferencia AS Referencia, @ArmazemID AS ArmazemID, 'INSERIDO' AS Acao;
        END
    END TRY
    BEGIN CATCH
        THROW;
        RETURN;
    END CATCH
END
GO

-- =============================================
-- SP: InserirNovoVendedor
-- Descrição: Insere um novo vendedor no sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovoVendedor
    @PessoaCc VARCHAR(20),
    @CargoId INT,
    @NumVendas INT = 0
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Pessoa WHERE Cc = @PessoaCc)
        BEGIN
            RAISERROR('Pessoa não encontrada.', 16, 1)
            RETURN
        END

        IF NOT EXISTS (SELECT 1 FROM dbo.Cargo WHERE Id = @CargoId)
        BEGIN
            RAISERROR('Cargo não encontrado.', 16, 1)
            RETURN
        END

        IF EXISTS (SELECT 1 FROM dbo.Vendedor WHERE Pessoa_Cc = @PessoaCc)
        BEGIN
            RAISERROR('Esta pessoa já está registada como vendedor.', 16, 1)
            RETURN
        END

        INSERT INTO dbo.Vendedor (Pessoa_Cc, NumVendas, Cargo_Id)
        VALUES (@PessoaCc, @NumVendas, @CargoId);
        
        SELECT @PessoaCc AS PessoaCc, 'INSERIDO' AS Acao;
    END TRY
    BEGIN CATCH
        THROW;
        RETURN;
    END CATCH
END
GO

-- =============================================
-- SP: ObterVendasPorLoja
-- Descrição: Obtém as vendas filtradas por loja
-- =============================================
CREATE OR ALTER PROCEDURE dbo.ObterVendasPorLoja
    @LojaID INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        V.Id, V.DataHora, V.ValorTotal, V.MetodoPagamento, V.Cliente_Nif, L.Id
    FROM
        dbo.Venda V
    INNER JOIN
        dbo.Loja L ON V.Loja_Id = L.Id
    WHERE
        (@LojaID IS NULL OR V.Loja_Id = @LojaID)
    ORDER BY
        V.DataHora DESC;
END
GO