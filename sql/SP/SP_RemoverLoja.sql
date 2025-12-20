-- =============================================
-- SP: RemoverLoja
-- Descrição: Remove uma loja do sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.RemoverLoja
    @Id INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Loja WHERE Id = @Id)
        BEGIN
            RAISERROR('Loja não encontrada.', 16, 1);
            RETURN;
        END
        
        DELETE FROM dbo.Loja WHERE Id = @Id;
        PRINT 'Loja removida com sucesso!';
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
