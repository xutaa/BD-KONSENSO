-- =============================================
-- SP: AtualizarEmpresa
-- =============================================
USE p2g4;
GO

CREATE OR ALTER PROCEDURE dbo.AtualizarEmpresa
    @Nif VARCHAR(9),
    @Nome VARCHAR(100),
    @Localizacao VARCHAR(100),
    @NumTelefone VARCHAR(20),
    @Email VARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.Empresa
    SET Nome = @Nome, Localizacao = @Localizacao, 
        NumTelefone = @NumTelefone, Email = @Email
    WHERE Nif = @Nif;
END
GO
