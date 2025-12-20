-- =============================================
-- SP: InserirNovoVendedor
-- Descrição: Insere um novo vendedor no sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovoVendedor
    @Cc VARCHAR(20),
    @Nome VARCHAR(100),
    @Email VARCHAR(100),
    @DataNasc DATE,
    @Morada VARCHAR(200),
    @Telemovel VARCHAR(20),
    @CargoId INT,
    @EmpresaNif VARCHAR(20),
    @DataFim DATE
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

        IF EXISTS (SELECT 1 FROM dbo.Vendedor WHERE Pessoa_Cc = @Cc)
        BEGIN
            RAISERROR('Esta pessoa já está registada como vendedor.', 16, 1);
            ROLLBACK TRANSACTION; RETURN;
        END
    
        INSERT INTO dbo.Vendedor (Pessoa_Cc, NumVendas, Cargo_Id)
        VALUES (@Cc, 0, @CargoId);

        DECLARE @NovoVendedorId INT = SCOPE_IDENTITY();
        INSERT INTO dbo.ContratoVendedor (DataIn, Empresa_Nif, Vendedor_Id, DataFim)
        VALUES (GETDATE(), @EmpresaNif, @NovoVendedorId, @DataFim);

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
