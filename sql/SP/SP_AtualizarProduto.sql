-- =============================================
-- SP: AtualizarProduto
-- Descrição: Atualiza os dados de um produto existente
-- Nota: A Referência não é atualizável pois é a chave primária
-- =============================================
USE p2g4;
GO

CREATE OR ALTER PROCEDURE dbo.AtualizarProduto
    @Referencia VARCHAR(20),
    @Nome VARCHAR(100),
    @Descricao VARCHAR(200),
    @Preco DECIMAL(10, 2),
    @MaquinaId INT,
    @DistribuidoraId INT
AS
BEGIN
    SET NOCOUNT ON;
   
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Produto WHERE Referencia = @Referencia)
        BEGIN
            RAISERROR('Produto não encontrado.', 16, 1);
            RETURN;
        END
   
        UPDATE dbo.Produto
        SET Nome = @Nome,
            Descricao = @Descricao,
            Preco = @Preco,
            Maquina_Id = @MaquinaId,
            Distribuidora_Id = @DistribuidoraId
        WHERE Referencia = @Referencia;
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
