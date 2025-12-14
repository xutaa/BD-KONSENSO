CREATE OR ALTER PROCEDURE dbo.InserirNovoCliente
    @PessoaCc VARCHAR(20),
    @Nif VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Pessoa WHERE Cc = @PessoaCc)
        BEGIN
            RAISERROR('Pessoa não encontrada.', 16, 1)
            RETURN
        END

        IF EXISTS (SELECT 1 FROM dbo.Cliente WHERE Pessoa_Cc = @PessoaCc)
        BEGIN
            RAISERROR('Esta pessoa já está registada como cliente.', 16, 1)
            RETURN
        END

        IF EXISTS (SELECT 1 FROM dbo.Cliente WHERE Nif = @Nif)
        BEGIN
            RAISERROR('NIF já existe no sistema.', 16, 1)
            RETURN
        END

        INSERT INTO dbo.Cliente (Pessoa_Cc, Nif)
        VALUES (@PessoaCc, @Nif);
        
        SELECT @PessoaCc AS PessoaCc, 'INSERIDO' AS Acao;
    END TRY
    BEGIN CATCH
        THROW;
        RETURN;
    END CATCH
END
GO