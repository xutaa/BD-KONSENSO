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
