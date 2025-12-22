-- =============================================
-- SP: AtualizarMateriaPrima
-- =============================================
USE p2g4;
GO

CREATE OR ALTER PROCEDURE dbo.AtualizarMateriaPrima
    @Referencia VARCHAR(20),
    @Descricao VARCHAR(200),
    @Fornecedor_Id INT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.MateriaPrima
    SET Descricao = @Descricao, Fornecedor_Id = @Fornecedor_Id
    WHERE Referencia = @Referencia;
END
GO
