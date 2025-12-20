-- =============================================
-- SP: RemoverFornecedor
-- Descrição: Remove um fornecedor do sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.RemoverFornecedor
    @Id INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Fornecedor WHERE Id = @Id)
        BEGIN
            RAISERROR('Fornecedor não encontrado.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.MateriaPrima WHERE Fornecedor_Id = @Id)
        BEGIN
            RAISERROR('Não é possível remover este fornecedor pois existem matérias-primas associadas.', 16, 1);
            RETURN;
        END
        
        DELETE FROM dbo.Fornecedor WHERE Id = @Id;
        PRINT 'Fornecedor removido com sucesso!';
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
