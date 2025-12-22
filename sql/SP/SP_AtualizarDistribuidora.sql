-- =============================================
-- SP: AtualizarDistribuidora
-- =============================================
USE p2g4;
GO

CREATE OR ALTER PROCEDURE dbo.AtualizarDistribuidora
    @Id INT,
    @Nome VARCHAR(100),
    @Localizacao VARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.Distribuidora
    SET Nome = @Nome, Localizacao = @Localizacao
    WHERE Id = @Id;
END
GO
