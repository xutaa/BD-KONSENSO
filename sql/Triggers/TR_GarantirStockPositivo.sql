-- =============================================
-- Trigger: GarantirStockPositivo
-- Descrição: Verifica se há stock suficiente após atualização.
-- =============================================
CREATE OR ALTER TRIGGER GarantirStockPositivo
ON dbo.Stock
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (
        SELECT 1 
        FROM inserted 
        WHERE Quantidade < 0
    )
    BEGIN
        RAISERROR('Operação Abortada: Stock insuficiente para concluir a ação.', 16, 1);
        ROLLBACK TRANSACTION;
    END
END
GO
