-- =============================================
-- SP: RemoverMateriaPrima
-- Descrição: Remove uma matéria-prima do sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.RemoverMateriaPrima
    @Referencia VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.MateriaPrima WHERE Referencia = @Referencia)
        BEGIN
            RAISERROR('Matéria-prima não encontrada.', 16, 1);
            RETURN;
        END
        
        DELETE FROM dbo.MateriaPrima WHERE Referencia = @Referencia;
        PRINT 'Matéria-prima removida com sucesso!';
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
