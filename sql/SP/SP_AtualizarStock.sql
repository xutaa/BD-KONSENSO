-- =============================================
-- SP: AtualizarStock
-- =============================================
USE p2g4;
GO

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
