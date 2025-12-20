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
