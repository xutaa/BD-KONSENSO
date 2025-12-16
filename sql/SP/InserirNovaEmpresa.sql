CREATE OR ALTER PROCEDURE dbo.InserirNovaEmpresa
    @Nif VARCHAR(20),
    @Nome VARCHAR(100),
    @Localizacao VARCHAR(200),
    @NumTelefone VARCHAR(20),
    @Email VARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        IF LTRIM(RTRIM(@Nif)) = '' OR LTRIM(RTRIM(@Nome)) = ''
        BEGIN
            RAISERROR('NIF e Nome são obrigatórios.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Empresa WHERE Nif = @Nif)
        BEGIN
            RAISERROR('Já existe uma empresa com este NIF.', 16, 1);
            RETURN;
        END
        
        IF @Email IS NOT NULL AND @Email NOT LIKE '%_@__%.__%'
        BEGIN
            RAISERROR('Email inválido.', 16, 1);
            RETURN;
        END
        
        INSERT INTO dbo.Empresa (Nif, Nome, Localizacao, NumTelefone, Email)
        VALUES (@Nif, @Nome, @Localizacao, @NumTelefone, @Email);
        
        PRINT 'Empresa inserida com sucesso!';
        
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO