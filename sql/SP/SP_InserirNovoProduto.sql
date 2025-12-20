-- =============================================
-- SP: InserirNovoProduto
-- Descrição: Insere um novo produto no sistema
-- =============================================
CREATE OR ALTER PROCEDURE dbo.InserirNovoProduto
    @Referencia VARCHAR(20),
    @Descricao VARCHAR(200),
    @NomeProduto VARCHAR(100),
    @Preco DECIMAL(10, 2),
    @MaquinaID INT,
    @DistribuidoraID INT
AS
BEGIN
    SET NOCOUNT ON;

    IF @Preco <= 0.00
    BEGIN
        RAISERROR('O preço deve ser um valor positivo.', 16, 1) 
        RETURN
    END

    BEGIN TRY
        INSERT INTO dbo.Produto (Referencia, Descricao, NomeProduto, Preco, MaquinaID, DistribuidoraID)
        VALUES (@Referencia, @Descricao, @NomeProduto, @Preco, @MaquinaID, @DistribuidoraID);
        SELECT SCOPE_IDENTITY() AS ProdutoID; 
    END TRY
    BEGIN CATCH
        THROW;
        RETURN;
    END CATCH
END
GO
