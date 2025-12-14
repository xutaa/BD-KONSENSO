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