-- =============================================
-- SP: RemoverFuncionario
-- Descrição: Remove um funcionário do sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.RemoverFuncionario
    @Cc VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Funcionario WHERE Pessoa_Cc = @Cc)
        BEGIN
            RAISERROR('Funcionário não encontrado.', 16, 1);
            ROLLBACK TRANSACTION;
            RETURN;
        END
        
        DELETE FROM dbo.Funcionario WHERE Pessoa_Cc = @Cc;
        DELETE FROM dbo.Pessoa WHERE Cc = @Cc;
        
        COMMIT TRANSACTION;
        PRINT 'Funcionário removido com sucesso!';
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
