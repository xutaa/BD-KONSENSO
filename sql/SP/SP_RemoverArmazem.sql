-- =============================================
-- SP: RemoverArmazem
-- Descrição: Remove um armazém do sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.RemoverArmazem
    @Id INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Armazem WHERE Id = @Id)
        BEGIN
            RAISERROR('Armazém não encontrado.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Stock WHERE Armazem_Id = @Id)
        BEGIN
            RAISERROR('Não é possível remover este armazém pois existe stock associado.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Loja WHERE Armazem_Id = @Id)
        BEGIN
            RAISERROR('Não é possível remover este armazém pois existem lojas associadas.', 16, 1);
            RETURN;
        END
        
        DELETE FROM dbo.Armazem WHERE Id = @Id;
        PRINT 'Armazém removido com sucesso!';
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
