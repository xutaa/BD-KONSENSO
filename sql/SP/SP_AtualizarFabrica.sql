-- =============================================
-- SP: AtualizarFabrica
-- =============================================
USE p2g4;
GO

CREATE OR ALTER PROCEDURE dbo.AtualizarFabrica
    @Id INT,
    @Nome VARCHAR(100),
    @Localizacao VARCHAR(100),
    @Empresa_Nif VARCHAR(9),
    @Distribuidora_Id INT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.Fabrica
    SET Nome = @Nome, Localizacao = @Localizacao, 
        Empresa_Nif = @Empresa_Nif, Distribuidora_Id = @Distribuidora_Id
    WHERE Id = @Id;
END
GO
