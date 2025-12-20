-- =============================================
-- SP: InserirNovaDistribuidora
-- Descrição: Insere uma nova distribuidora no sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovaDistribuidora
    @Nome VARCHAR(100),
    @Localizacao VARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        IF LTRIM(RTRIM(@Nome)) = '' OR LTRIM(RTRIM(@Localizacao)) = ''
        BEGIN
            RAISERROR('Nome e Localização são obrigatórios.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Distribuidora WHERE Nome = @Nome)
        BEGIN
            RAISERROR('Já existe uma distribuidora com este nome.', 16, 1);
            RETURN;
        END
        
        INSERT INTO dbo.Distribuidora (Nome, Localizacao)
        VALUES (@Nome, @Localizacao);
        
        SELECT SCOPE_IDENTITY() AS NovoId;
        PRINT 'Distribuidora inserida com sucesso!';
        
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(2056) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
