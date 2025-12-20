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
