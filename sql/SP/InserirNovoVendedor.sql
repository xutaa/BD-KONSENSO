CREATE OR ALTER PROCEDURE dbo.InserirNovoVendedor
    @PessoaCc VARCHAR(20),
    @CargoId INT,
    @NumVendas INT = 0
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Pessoa WHERE Cc = @PessoaCc)
        BEGIN
            RAISERROR('Pessoa não encontrada.', 16, 1)
            RETURN
        END

        IF NOT EXISTS (SELECT 1 FROM dbo.Cargo WHERE Id = @CargoId)
        BEGIN
            RAISERROR('Cargo não encontrado.', 16, 1)
            RETURN
        END

        IF EXISTS (SELECT 1 FROM dbo.Vendedor WHERE Pessoa_Cc = @PessoaCc)
        BEGIN
            RAISERROR('Esta pessoa já está registada como vendedor.', 16, 1)
            RETURN
        END

        INSERT INTO dbo.Vendedor (Pessoa_Cc, NumVendas, Cargo_Id)
        VALUES (@PessoaCc, @NumVendas, @CargoId);
        
        SELECT @PessoaCc AS PessoaCc, 'INSERIDO' AS Acao;
    END TRY
    BEGIN CATCH
        THROW;
        RETURN;
    END CATCH
END
GO