-- =============================================
-- SP: InserirNovoItem
-- Descrição: Insere um novo item numa venda
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovoItem
    @VendaId INT,
    @ProdutoReferencia VARCHAR(20),
    @Quantidade INT,
    @Preco DECIMAL(10, 2)
AS
BEGIN
    SET NOCOUNT ON;

    IF @Quantidade <= 0
    BEGIN
        RAISERROR('A quantidade deve ser maior que zero.', 16, 1)
        RETURN
    END

    IF @Preco <= 0
    BEGIN
        RAISERROR('O preço deve ser maior que zero.', 16, 1)
        RETURN
    END

    BEGIN TRY
        IF NOT EXISTS (SELECT 1 FROM dbo.Venda WHERE Id = @VendaId)
        BEGIN
            RAISERROR('Venda não encontrada.', 16, 1)
            RETURN
        END

        IF NOT EXISTS (SELECT 1 FROM dbo.Produto WHERE Referencia = @ProdutoReferencia)
        BEGIN
            RAISERROR('Produto não encontrado.', 16, 1)
            RETURN
        END

        IF EXISTS (SELECT 1 FROM dbo.Item WHERE Venda_Id = @VendaId AND Produto_Referencia = @ProdutoReferencia)
        BEGIN
            RAISERROR('Este produto já foi adicionado a esta venda.', 16, 1)
            RETURN
        END

        INSERT INTO dbo.Item (Venda_Id, Produto_Referencia, Quantidade, Preco)
        VALUES (@VendaId, @ProdutoReferencia, @Quantidade, @Preco);
        
        SELECT @VendaId AS VendaId, @ProdutoReferencia AS Referencia, 'INSERIDO' AS Acao;
    END TRY
    BEGIN CATCH
        THROW;
        RETURN;
    END CATCH
END
GO
