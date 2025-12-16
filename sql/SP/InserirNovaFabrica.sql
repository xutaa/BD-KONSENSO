CREATE OR ALTER PROCEDURE dbo.InserirNovaFabrica
    @Nome VARCHAR(100),
    @Localizacao VARCHAR(200),
    @EmpresaNif VARCHAR(20),
    @DistribuidoraId INT
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        IF LTRIM(RTRIM(@Nome)) = '' OR LTRIM(RTRIM(@Localizacao)) = ''
        BEGIN
            RAISERROR('Nome e Localização são obrigatórios.', 16, 1);
            RETURN;
        END
        
        IF NOT EXISTS (SELECT 1 FROM dbo.Empresa WHERE Nif = @EmpresaNif)
        BEGIN
            RAISERROR('Empresa não existe.', 16, 1);
            RETURN;
        END
        
        IF NOT EXISTS (SELECT 1 FROM dbo.Distribuidora WHERE Id = @DistribuidoraId)
        BEGIN
            RAISERROR('Distribuidora não existe.', 16, 1);
            RETURN;
        END
        
        INSERT INTO dbo.Fabrica (Nome, Localizacao, Empresa_Nif, Distribuidora_Id)
        VALUES (@Nome, @Localizacao, @EmpresaNif, @DistribuidoraId);
        
        PRINT 'Fábrica inserida com sucesso!';
        
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO