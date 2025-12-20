-- =============================================
-- SP: RemoverCargo
-- Descrição: Remove um cargo do sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.RemoverCargo
    @Id INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Cargo WHERE Id = @Id)
        BEGIN
            RAISERROR('Cargo não encontrado.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Funcionario WHERE Cargo_Id = @Id)
        BEGIN
            RAISERROR('Não é possível remover este cargo pois existem funcionários associados.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Vendedor WHERE Cargo_Id = @Id)
        BEGIN
            RAISERROR('Não é possível remover este cargo pois existem vendedores associados.', 16, 1);
            RETURN;
        END
        
        DELETE FROM dbo.Cargo WHERE Id = @Id;
        PRINT 'Cargo removido com sucesso!';
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
