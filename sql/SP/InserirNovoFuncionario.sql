CREATE OR ALTER PROCEDURE dbo.InserirNovoFuncionario
    @PessoaCc VARCHAR(20),
    @CargoId INT,
    @EmpresaNif VARCHAR(20),
    @FabricaId INT = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Pessoa WHERE Cc = @PessoaCc)
        BEGIN
            RAISERROR('Pessoa com este CC não existe.', 16, 1);
            RETURN;
        END
        
        IF NOT EXISTS (SELECT 1 FROM dbo.Cargo WHERE Id = @CargoId)
        BEGIN
            RAISERROR('Cargo não existe.', 16, 1);
            RETURN;
        END
        
        IF NOT EXISTS (SELECT 1 FROM dbo.Empresa WHERE Nif = @EmpresaNif)
        BEGIN
            RAISERROR('Empresa não existe.', 16, 1);
            RETURN;
        END
        
        IF EXISTS (SELECT 1 FROM dbo.Funcionario WHERE Pessoa_Cc = @PessoaCc)
        BEGIN
            RAISERROR('Esta pessoa já é um funcionário.', 16, 1);
            RETURN;
        END
        
        IF @FabricaId IS NOT NULL AND NOT EXISTS (SELECT 1 FROM dbo.Fabrica WHERE Id = @FabricaId)
        BEGIN
            RAISERROR('Fábrica não existe.', 16, 1);
            RETURN;
        END
        
        INSERT INTO dbo.Funcionario (Pessoa_Cc, Cargo_Id, Empresa_Nif, Fabrica_Id)
        VALUES (@PessoaCc, @CargoId, @EmpresaNif, @FabricaId);
        
        PRINT 'Funcionário inserido com sucesso!';
        
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO