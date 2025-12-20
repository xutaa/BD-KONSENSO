-- =============================================
-- SP: InserirNovoCliente
-- Descrição: Insere um novo cliente no sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovoCliente
    @Cc VARCHAR(20),
    @Nome VARCHAR(100),
    @Email VARCHAR(100),
    @DataNasc DATE,
    @Morada VARCHAR(200),
    @Telemovel VARCHAR(20),
    @Nif VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRANSACTION;
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Pessoa WHERE Cc = @Cc)
        BEGIN
            INSERT INTO dbo.Pessoa (Cc, Nome, Email, DataNascimento, Morada, NumTelefone)
            VALUES (@Cc, @Nome, @Email, @DataNasc, @Morada, @Telemovel);
        END

        IF EXISTS (SELECT 1 FROM dbo.Cliente WHERE Pessoa_Cc = @Cc)
        BEGIN
            RAISERROR('Esta pessoa já está registada como cliente.', 16, 1);
            ROLLBACK TRANSACTION; RETURN;
        END

        IF EXISTS (SELECT 1 FROM dbo.Cliente WHERE Nif = @Nif)
        BEGIN
            RAISERROR('Este NIF já está atribuído a outro cliente.', 16, 1);
            ROLLBACK TRANSACTION; RETURN;
        END

        INSERT INTO dbo.Cliente (Pessoa_Cc, Nif)
        VALUES (@Cc, @Nif);

        COMMIT TRANSACTION;
        SELECT @Cc AS PessoaCc, 'SUCESSO' AS Status;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        DECLARE @ErrorMessage NVARCHAR(2056) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
