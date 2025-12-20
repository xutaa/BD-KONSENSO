-- =============================================
-- SP: ObterItensVenda
-- Descrição: Obtém os itens de uma venda específica
-- =============================================
CREATE OR ALTER PROCEDURE dbo.ObterItensVenda
    @VendaId INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Venda WHERE Id = @VendaId)
        BEGIN
            RAISERROR('Venda não encontrada.', 16, 1)
            RETURN
        END
        SELECT P.Nome, I.Quantidade, I.Preco, (I.Quantidade * I.Preco) as Total
        FROM Item I
        JOIN Produto P ON I.Produto_Referencia = P.Referencia
        WHERE I.Venda_Id = @VendaId;
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(2056) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
