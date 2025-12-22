-- =============================================
-- SP: AtualizarCliente
-- =============================================
USE p2g4;
GO

CREATE OR ALTER PROCEDURE dbo.AtualizarCliente
    @Pessoa_Cc VARCHAR(20),
    @Nome VARCHAR(100),
    @Email VARCHAR(100),
    @DataNascimento DATE,
    @Morada VARCHAR(200),
    @NumTelefone VARCHAR(20),
    @Nif VARCHAR(9)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Atualizar dados na tabela Pessoa
        UPDATE dbo.Pessoa
        SET Nome = @Nome, Email = @Email, DataNascimento = @DataNascimento, 
            Morada = @Morada, NumTelefone = @NumTelefone
        WHERE Cc = @Pessoa_Cc;
        
        -- Atualizar NIF na tabela Cliente
        UPDATE dbo.Cliente
        SET Nif = @Nif
        WHERE Pessoa_Cc = @Pessoa_Cc;
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO
