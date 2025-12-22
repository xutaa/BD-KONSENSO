-- =============================================
-- SP: AtualizarCargo
-- =============================================
USE p2g4;
GO

CREATE OR ALTER PROCEDURE dbo.AtualizarCargo
    @Id INT,
    @Nome VARCHAR(100),
    @Descricao VARCHAR(200)
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.Cargo
    SET Nome = @Nome, Descricao = @Descricao
    WHERE Id = @Id;
END
GO
