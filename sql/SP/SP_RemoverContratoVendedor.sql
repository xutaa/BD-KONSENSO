-- =============================================
-- SP: RemoverContratoVendedor
-- Descrição: Remove um contrato de vendedor
-- =============================================
CREATE OR ALTER PROCEDURE dbo.RemoverContratoVendedor
    @VendedorId INT,
    @EmpresaNif VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        IF NOT EXISTS (
            SELECT 1 FROM dbo.ContratoVendedor 
            WHERE Vendedor_Id = @VendedorId AND Empresa_Nif = @EmpresaNif
        )
        BEGIN
            RAISERROR('Contrato de vendedor não encontrado.', 16, 1);
            RETURN;
        END
        
        DELETE FROM dbo.ContratoVendedor 
        WHERE Vendedor_Id = @VendedorId AND Empresa_Nif = @EmpresaNif;
        
        PRINT 'Contrato de vendedor removido com sucesso!';
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
