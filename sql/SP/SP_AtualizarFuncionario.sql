-- =============================================
-- SP: AtualizarFuncionario
-- =============================================
USE p2g4;
GO

CREATE OR ALTER PROCEDURE dbo.AtualizarFuncionario
    @Pessoa_Cc VARCHAR(20),
    @Nome VARCHAR(100),
    @Email VARCHAR(100),
    @DataNascimento DATE,
    @Morada VARCHAR(200),
    @NumTelefone VARCHAR(20),
    @Cargo_Id INT,
    @Empresa_Nif VARCHAR(9),
    @Fabrica_Id INT = NULL
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        UPDATE dbo.Pessoa
        SET Nome = @Nome, Email = @Email, DataNascimento = @DataNascimento, 
            Morada = @Morada, NumTelefone = @NumTelefone
        WHERE Cc = @Pessoa_Cc;
        
        UPDATE dbo.Funcionario
        SET Cargo_Id = @Cargo_Id, Empresa_Nif = @Empresa_Nif, Fabrica_Id = @Fabrica_Id
        WHERE Pessoa_Cc = @Pessoa_Cc;
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO
