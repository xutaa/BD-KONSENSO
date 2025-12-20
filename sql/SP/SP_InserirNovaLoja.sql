-- =============================================
-- SP: InserirNovaLoja
-- Descrição: Insere uma nova loja no sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovaLoja
    @Nome VARCHAR(100),
    @Localizacao VARCHAR(100),
    @ArmazemId INT
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        IF LTRIM(RTRIM(@Nome)) = '' OR LTRIM(RTRIM(@Localizacao)) = ''
        BEGIN
            RAISERROR('Nome e Localização são obrigatórios.', 16, 1);
            RETURN;
        END
        
        IF NOT EXISTS (SELECT 1 FROM dbo.Armazem WHERE Id = @ArmazemId)
        BEGIN
            RAISERROR('Armazém não existe.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Loja WHERE Nome = @Nome AND Localizacao = @Localizacao)
        BEGIN
            RAISERROR('Já existe uma loja com este nome nesta localização.', 16, 1);
            RETURN;
        END
        
        INSERT INTO dbo.Loja (Nome, Localizacao, Armazem_Id)
        VALUES (@Nome, @Localizacao, @ArmazemId);
        
        SELECT SCOPE_IDENTITY() AS NovoId;
        PRINT 'Loja inserida com sucesso!';
        
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(2056) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
