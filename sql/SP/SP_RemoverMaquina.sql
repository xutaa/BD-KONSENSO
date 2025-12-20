-- =============================================
-- SP: RemoverMaquina
-- Descrição: Remove uma máquina do sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.RemoverMaquina
    @Id INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Maquina WHERE Id = @Id)
        BEGIN
            RAISERROR('Máquina não encontrada.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Produto WHERE MaquinaID = @Id)
        BEGIN
            RAISERROR('Não é possível remover esta máquina pois existem produtos associados.', 16, 1);
            RETURN;
        END
        
        DELETE FROM dbo.Maquina WHERE Id = @Id;
        PRINT 'Máquina removida com sucesso!';
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
