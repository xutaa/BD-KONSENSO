-- =============================================
-- SP: TransferirStock
-- Descrição: Transfere stock entre dois armazéns
-- =============================================
CREATE OR ALTER PROCEDURE dbo.TransferirStock
    @ProdutoRef VARCHAR(20),
    @ArmazemOrigem INT,
    @ArmazemDestino INT,
    @Quantidade INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        UPDATE Stock SET Quantidade = Quantidade - @Quantidade 
        WHERE Produto_Referencia = @ProdutoRef AND Armazem_Id = @ArmazemOrigem;
        
        UPDATE Stock SET Quantidade = Quantidade + @Quantidade 
        WHERE Produto_Referencia = @ProdutoRef AND Armazem_Id = @ArmazemDestino;
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO
