-- =============================================
-- SP: InserirNovoContratoVendedor
-- Descrição: Insere um novo contrato de vendedor
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovoContratoVendedor
    @VendedorId INT,
    @EmpresaNif VARCHAR(20),
    @DataIn DATE
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Vendedor WHERE Id = @VendedorId)
        BEGIN
            RAISERROR('Vendedor não existe.', 16, 1);
            RETURN;
        END
        
        IF NOT EXISTS (SELECT 1 FROM dbo.Empresa WHERE Nif = @EmpresaNif)
        BEGIN
            RAISERROR('Empresa não existe.', 16, 1);
            RETURN;
        END
        
        IF @DataIn > GETDATE()
        BEGIN
            RAISERROR('A data de início não pode ser futura.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (
            SELECT 1 
            FROM dbo.ContratoVendedor 
            WHERE Vendedor_Id = @VendedorId 
              AND Empresa_Nif = @EmpresaNif
        )
        BEGIN
            RAISERROR('Já existe um contrato para este vendedor nesta empresa.', 16, 1);
            RETURN;
        END
        
        INSERT INTO dbo.ContratoVendedor (DataIn, Empresa_Nif, Vendedor_Id)
        VALUES (@DataIn, @EmpresaNif, @VendedorId);
        
        PRINT 'Contrato de vendedor inserido com sucesso!';
        
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(2056) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
