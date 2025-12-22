-- =============================================
-- SP: AtualizarVendedor
-- =============================================
USE p2g4;
GO

CREATE OR ALTER PROCEDURE dbo.AtualizarVendedor
    @Pessoa_Cc VARCHAR(20),
    @Nome VARCHAR(100),
    @Email VARCHAR(100),
    @DataNascimento DATE,
    @Morada VARCHAR(200),
    @NumTelefone VARCHAR(20),
    @Cargo_Id INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        UPDATE dbo.Pessoa
        SET Nome = @Nome, Email = @Email, DataNascimento = @DataNascimento, 
            Morada = @Morada, NumTelefone = @NumTelefone
        WHERE Cc = @Pessoa_Cc;
        
        UPDATE dbo.Vendedor
        SET Cargo_Id = @Cargo_Id
        WHERE Pessoa_Cc = @Pessoa_Cc;
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO
