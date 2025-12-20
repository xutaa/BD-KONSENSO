-- =============================================
-- SP: RemoverFabrica
-- Descrição: Remove uma fábrica do sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.RemoverFabrica
    @Id INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Fabrica WHERE Id = @Id)
        BEGIN
            RAISERROR('Fábrica não encontrada.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Maquina WHERE Fabrica_Id = @Id)
        BEGIN
            RAISERROR('Não é possível remover esta fábrica pois existem máquinas associadas.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Funcionario WHERE Fabrica_Id = @Id)
        BEGIN
            RAISERROR('Não é possível remover esta fábrica pois existem funcionários associados.', 16, 1);
            RETURN;
        END
        
        DELETE FROM dbo.Fabrica WHERE Id = @Id;
        PRINT 'Fábrica removida com sucesso!';
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
