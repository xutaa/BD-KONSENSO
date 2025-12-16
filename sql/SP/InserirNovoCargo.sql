CREATE OR ALTER PROCEDURE dbo.InserirNovoCargo
    @Nome VARCHAR(100),
    @Descricao VARCHAR(200) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        IF LTRIM(RTRIM(@Nome)) = ''
        BEGIN
            RAISERROR('O nome do cargo não pode estar vazio.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Cargo WHERE Nome = @Nome)
        BEGIN
            RAISERROR('Já existe um cargo com este nome.', 16, 1);
            RETURN;
        END
        
        INSERT INTO dbo.Cargo (Nome, Descricao)
        VALUES (@Nome, @Descricao);
        
        PRINT 'Cargo inserido com sucesso!';
        
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO