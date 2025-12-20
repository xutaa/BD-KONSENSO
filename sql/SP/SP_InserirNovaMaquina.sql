-- =============================================
-- SP: InserirNovaMaquina
-- Descrição: Insere uma nova máquina no sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovaMaquina
    @Descricao VARCHAR(200),
    @Tipo VARCHAR(50),
    @FabricaId INT
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        IF LTRIM(RTRIM(@Descricao)) = '' OR LTRIM(RTRIM(@Tipo)) = ''
        BEGIN
            RAISERROR('Descrição e Tipo são obrigatórios.', 16, 1);
            RETURN;
        END
        
        IF NOT EXISTS (SELECT 1 FROM dbo.Fabrica WHERE Id = @FabricaId)
        BEGIN
            RAISERROR('Fábrica não existe.', 16, 1);
            RETURN;
        END
        
        INSERT INTO dbo.Maquina (Descricao, Tipo, Fabrica_Id)
        VALUES (@Descricao, @Tipo, @FabricaId);
        
        PRINT 'Máquina inserida com sucesso!';
        
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(2056) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
