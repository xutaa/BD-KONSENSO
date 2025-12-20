-- =============================================
-- SP: AtualizarProduto
-- Descrição: Atualiza os dados de um produto existente
-- =============================================
CREATE OR ALTER PROCEDURE dbo.AtualizarProduto
    @ReferenciaAtual VARCHAR(20),
    @NovaReferencia VARCHAR(20),
    @Nome VARCHAR(100),
    @Descricao VARCHAR(200),
    @Preco DECIMAL(10, 2),
    @MaquinaId INT,
    @DistribuidoraId INT
AS
BEGIN
    SET NOCOUNT ON;
   
    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Produto WHERE Referencia = @ReferenciaAtual)
        BEGIN
            RAISERROR('Produto não encontrado.', 16, 1);
            RETURN;
        END
   
        IF @ReferenciaAtual <> @NovaReferencia AND EXISTS (SELECT 1 FROM dbo.Produto WHERE Referencia = @NovaReferencia)
        BEGIN
            RAISERROR('A nova referência já existe em outro produto.', 16, 1);
            RETURN;
        END
   
        UPDATE dbo.Produto
        SET Referencia = @NovaReferencia,
            Nome = @Nome,
            Descricao = @Descricao,
            Preco = @Preco,
            MaquinaID = @MaquinaId,
            DistribuidoraID = @DistribuidoraId
        WHERE Referencia = @ReferenciaAtual;
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
