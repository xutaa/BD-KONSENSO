-- =============================================
-- SP: RemoverVendedor
-- Descrição: Remove um vendedor do sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.RemoverVendedor
    @Cc VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Vendedor WHERE Pessoa_Cc = @Cc)
        BEGIN
            RAISERROR('Vendedor não encontrado.', 16, 1);
            ROLLBACK TRANSACTION;
            RETURN;
        END
        
        DECLARE @VendedorId INT;
        SELECT @VendedorId = Id FROM dbo.Vendedor WHERE Pessoa_Cc = @Cc;
        
        DELETE FROM dbo.ContratoVendedor WHERE Vendedor_Id = @VendedorId;
        
        DELETE FROM dbo.Vendedor WHERE Pessoa_Cc = @Cc;
        DELETE FROM dbo.Pessoa WHERE Cc = @Cc;
        
        COMMIT TRANSACTION;
        PRINT 'Vendedor removido com sucesso!';
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
