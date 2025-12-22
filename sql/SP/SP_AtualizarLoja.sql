-- =============================================
-- SP: AtualizarLoja
-- =============================================
USE p2g4;
GO

CREATE OR ALTER PROCEDURE dbo.AtualizarLoja
    @Id INT,
    @Nome VARCHAR(100),
    @Localizacao VARCHAR(100),
    @Armazem_Id INT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.Loja
    SET Nome = @Nome, Localizacao = @Localizacao, Armazem_Id = @Armazem_Id
    WHERE Id = @Id;
END
GO
