-- =============================================
-- SP: RemoverStock
-- Descrição: Remove stock de um produto num armazém
-- =============================================
CREATE OR ALTER PROCEDURE dbo.RemoverStock
    @ProdutoReferencia VARCHAR(20),
    @ArmazemId INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        IF NOT EXISTS (
            SELECT 1 FROM dbo.Stock 
            WHERE Produto_Referencia = @ProdutoReferencia AND Armazem_Id = @ArmazemId
        )
        BEGIN
            RAISERROR('Registo de stock não encontrado.', 16, 1);
            RETURN;
        END
        
        DELETE FROM dbo.Stock 
        WHERE Produto_Referencia = @ProdutoReferencia AND Armazem_Id = @ArmazemId;
        
        PRINT 'Registo de stock removido com sucesso!';
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
