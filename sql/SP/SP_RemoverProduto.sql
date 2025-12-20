-- =============================================
-- SP: RemoverProduto
-- Descrição: Remove um produto do sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.RemoverProduto
    @Referencia VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Produto WHERE Referencia = @Referencia)
        BEGIN
            RAISERROR('Produto não encontrado.', 16, 1);
            RETURN;
        END
        IF EXISTS (SELECT 1 FROM dbo.Item WHERE Produto_Referencia = @Referencia)
        BEGIN
            RAISERROR('Não é possível remover este produto pois já existem vendas associadas.', 16, 1);
            RETURN;
        END
        DELETE FROM dbo.Produto WHERE Referencia = @Referencia;
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
