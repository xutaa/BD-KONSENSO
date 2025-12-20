-- =============================================
-- SP: InserirNovoFuncionario
-- Descrição: Insere um novo funcionário no sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovoFuncionario
    @Cc VARCHAR(20),
    @Nome VARCHAR(100),
    @Email VARCHAR(100),
    @DataNasc DATE,
    @Morada VARCHAR(200),
    @Telemovel VARCHAR(20),
    @CargoId INT,
    @EmpresaNif VARCHAR(20),
    @FabricaId INT = NULL
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        IF NOT EXISTS (SELECT 1 FROM dbo.Pessoa WHERE Cc = @Cc)
        BEGIN
            INSERT INTO dbo.Pessoa (Cc, Nome, Email, DataNascimento, Morada, NumTelefone)
            VALUES (@Cc, @Nome, @Email, @DataNasc, @Morada, @Telemovel);
        END

        IF EXISTS (SELECT 1 FROM dbo.Funcionario WHERE Pessoa_Cc = @Cc)
        BEGIN
            RAISERROR('Esta pessoa já está registada como funcionário.', 16, 1);
            ROLLBACK TRANSACTION; RETURN;
        END
    
        INSERT INTO dbo.Funcionario (Pessoa_Cc, Cargo_Id, Empresa_Nif, Fabrica_Id)
        VALUES (@Cc, @CargoId, @EmpresaNif, @FabricaId);

        COMMIT TRANSACTION;
        SELECT @Cc AS PessoaCc, 'SUCESSO' AS Status;
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(2056) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
