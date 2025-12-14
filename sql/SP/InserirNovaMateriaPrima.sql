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