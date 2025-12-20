-- =============================================
-- SP: RemoverDistribuidora
-- Descrição: Remove uma distribuidora do sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.RemoverDistribuidora
    @Id INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Distribuidora WHERE Id = @Id)
        BEGIN
            RAISERROR('Distribuidora não encontrada.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Fabrica WHERE Distribuidora_Id = @Id)
        BEGIN
            RAISERROR('Não é possível remover esta distribuidora pois existem fábricas associadas.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Produto WHERE DistribuidoraID = @Id)
        BEGIN
            RAISERROR('Não é possível remover esta distribuidora pois existem produtos associados.', 16, 1);
            RETURN;
        END
        
        DELETE FROM dbo.Distribuidora WHERE Id = @Id;
        PRINT 'Distribuidora removida com sucesso!';
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
