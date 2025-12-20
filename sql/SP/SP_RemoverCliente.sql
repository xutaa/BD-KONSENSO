-- =============================================
-- SP: RemoverCliente
-- Descrição: Remove um cliente do sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.RemoverCliente
    @Cc VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Cliente WHERE Pessoa_Cc = @Cc)
        BEGIN
            RAISERROR('Cliente não encontrado.', 16, 1);
            ROLLBACK TRANSACTION;
            RETURN;
        END
        
        -- Verificação feita pelo trigger TR_BloquearExclusaoClienteComVendas
        DELETE FROM dbo.Cliente WHERE Pessoa_Cc = @Cc;
        DELETE FROM dbo.Pessoa WHERE Cc = @Cc;
        
        COMMIT TRANSACTION;
        PRINT 'Cliente removido com sucesso!';
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
