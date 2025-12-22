-- =============================================
-- SP: AtualizarContratoVendedor
-- =============================================
USE p2g4;
GO

CREATE OR ALTER PROCEDURE dbo.AtualizarContratoVendedor
    @Vendedor_Id INT,
    @Empresa_Nif VARCHAR(20),
    @DataIn DATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.ContratoVendedor
    SET DataIn = @DataIn
    WHERE Vendedor_Id = @Vendedor_Id AND Empresa_Nif = @Empresa_Nif;
END
GO
