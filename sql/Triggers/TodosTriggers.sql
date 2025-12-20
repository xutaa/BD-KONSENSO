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


-- =============================================
-- Trigger: TR_ValidarCapacidadeArmazem
-- Descrição: Impede adicionar stock acima da capacidade do armazém
-- =============================================
CREATE OR ALTER TRIGGER TR_ValidarCapacidadeArmazem
ON dbo.Stock
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    
    IF EXISTS (
        SELECT 1 
        FROM dbo.Armazem a
        INNER JOIN (
            SELECT Armazem_Id, SUM(Quantidade) AS TotalStock
            FROM dbo.Stock
            GROUP BY Armazem_Id
        ) s ON a.Id = s.Armazem_Id
        WHERE s.TotalStock > a.Capacidade
          AND a.Id IN (SELECT Armazem_Id FROM inserted)
    )
    BEGIN
        RAISERROR('Operação cancelada: Capacidade do armazém excedida!', 16, 1);
        ROLLBACK TRANSACTION;
    END
END
GO

-- =============================================
-- Trigger: TR_BloquearExclusaoClienteComVendas
-- Descrição: Impede eliminar clientes com histórico de compras
-- =============================================
CREATE OR ALTER TRIGGER TR_BloquearExclusaoClienteComVendas
ON dbo.Cliente
INSTEAD OF DELETE
AS
BEGIN
    SET NOCOUNT ON;
    
    IF EXISTS (
        SELECT 1 FROM dbo.Venda WHERE Cliente_Nif IN (SELECT Nif FROM deleted)
    )
    BEGIN
        RAISERROR('Não é possível eliminar clientes com histórico de compras.', 16, 1);
        RETURN;
    END
    
    DELETE FROM dbo.Cliente WHERE Pessoa_Cc IN (SELECT Pessoa_Cc FROM deleted);
END
GO