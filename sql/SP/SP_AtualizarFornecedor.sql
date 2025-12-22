-- =============================================
-- SP: AtualizarFornecedor
-- =============================================
USE p2g4;
GO

CREATE OR ALTER PROCEDURE dbo.AtualizarFornecedor
    @Id INT,
    @Nome VARCHAR(100),
    @Empresa_Nif VARCHAR(9)
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.Fornecedor
    SET Nome = @Nome, Empresa_Nif = @Empresa_Nif
    WHERE Id = @Id;
END
GO
