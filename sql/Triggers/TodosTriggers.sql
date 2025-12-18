-- =============================================
-- Trigger: GarantirStockPositivo (nao usado)
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

-- =============================================
-- Trigger: AtualizarTotalVenda
-- Descrição: Atualiza o valor total da venda após inserção, atualização ou exclusão de itens.
-- =============================================
CREATE OR ALTER TRIGGER AtualizarTotalVenda
ON dbo.Item
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;
    
    UPDATE V
    SET V.ValorTotal = ISNULL((SELECT SUM(I.Quantidade * I.Preco) 
                               FROM dbo.Item I 
                               WHERE I.Venda_Id = V.Id), 0)
    FROM dbo.Venda V
    WHERE V.Id IN (SELECT Venda_Id FROM inserted UNION SELECT Venda_Id FROM deleted);
END
GO

-- =============================================
-- Trigger: MudarStockArmazemEliminado
-- Descrição: Muda o stock existente num armazem eliminado para o primeiro armazem.
-- =============================================
-- por implementar