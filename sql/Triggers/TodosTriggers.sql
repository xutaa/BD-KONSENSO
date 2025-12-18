-- =============================================
-- Trigger: VerificarStockVenda
-- Descrição: Verifica se há stock suficiente antes de inserir um item numa venda.
-- =============================================
CREATE OR ALTER TRIGGER VerificarStockVenda
ON dbo.Item
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (
        SELECT 1 
        FROM dbo.Stock s
        JOIN inserted i ON s.Produto_Referencia = i.Produto_Referencia
        JOIN dbo.Venda v ON i.Venda_Id = v.Id
        WHERE s.Armazem_Id = v.Loja_Id AND s.Quantidade < 0
    )
    BEGIN
        RAISERROR('Operação Cancelada: Stock insuficiente para concluir a venda.', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;
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
END;
GO

-- =============================================
-- Trigger: MudarStockArmazemEliminado
-- Descrição: Muda o stock existente num armazem eliminado para o primeiro armazem.
-- =============================================
-- por implementar