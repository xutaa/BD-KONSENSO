-- =============================================
-- SP: AtualizarMaquina
-- =============================================
USE p2g4;
GO

CREATE OR ALTER PROCEDURE dbo.AtualizarMaquina
    @Id INT,
    @Descricao VARCHAR(200),
    @Tipo VARCHAR(50),
    @Fabrica_Id INT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.Maquina
    SET Descricao = @Descricao, Tipo = @Tipo, Fabrica_Id = @Fabrica_Id
    WHERE Id = @Id;
END
GO
