-- =============================================
-- SP: InserirNovoArmazem
-- Descrição: Insere um novo armazém no sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovoArmazem
    @Localizacao VARCHAR(200),
    @Capacidade INT
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        IF LTRIM(RTRIM(@Localizacao)) = ''
        BEGIN
            RAISERROR('Localização é obrigatória.', 16, 1);
            RETURN;
        END
        
        IF @Capacidade <= 0
        BEGIN
            RAISERROR('Capacidade deve ser maior que zero.', 16, 1);
            RETURN;
        END
        
        INSERT INTO dbo.Armazem (Localizacao, Capacidade)
        VALUES (@Localizacao, @Capacidade);
        
        PRINT 'Armazém inserido com sucesso!';
        
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(2056) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
