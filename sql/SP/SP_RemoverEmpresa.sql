-- =============================================
-- SP: RemoverEmpresa
-- Descrição: Remove uma empresa do sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.RemoverEmpresa
    @Nif VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Empresa WHERE Nif = @Nif)
        BEGIN
            RAISERROR('Empresa não encontrada.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Fabrica WHERE Empresa_Nif = @Nif)
        BEGIN
            RAISERROR('Não é possível remover esta empresa pois existem fábricas associadas.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Funcionario WHERE Empresa_Nif = @Nif)
        BEGIN
            RAISERROR('Não é possível remover esta empresa pois existem funcionários associados.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Fornecedor WHERE Empresa_Nif = @Nif)
        BEGIN
            RAISERROR('Não é possível remover esta empresa pois existem fornecedores associados.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.ContratoVendedor WHERE Empresa_Nif = @Nif)
        BEGIN
            RAISERROR('Não é possível remover esta empresa pois existem contratos de vendedor associados.', 16, 1);
            RETURN;
        END
        
        DELETE FROM dbo.Empresa WHERE Nif = @Nif;
        PRINT 'Empresa removida com sucesso!';
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
