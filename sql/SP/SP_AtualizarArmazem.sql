-- =============================================
-- SP: AtualizarArmazem
-- =============================================
USE p2g4;
GO

CREATE OR ALTER PROCEDURE dbo.AtualizarArmazem
    @Id INT,
    @Localizacao VARCHAR(100),
    @Capacidade INT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.Armazem
    SET Localizacao = @Localizacao, Capacidade = @Capacidade
    WHERE Id = @Id;
END
GO
