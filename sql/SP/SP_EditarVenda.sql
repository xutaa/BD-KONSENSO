-- =============================================
-- Stored Procedure: SP_EditarVenda
-- Descrição: Edita uma venda existente (dados básicos e itens)
-- =============================================

CREATE OR ALTER PROCEDURE dbo.EditarVenda
    @Venda_Id INT,
    @Cliente_Nif VARCHAR(15) = NULL,
    @MetodoPagamento VARCHAR(50),
    @Itens dbo.ListaItensVenda READONLY
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        IF NOT EXISTS (SELECT 1 FROM Venda WHERE Id = @Venda_Id)
        BEGIN
            THROW 50001, 'Venda não encontrada.', 1;
        END
        
        DECLARE @ItensAntigos TABLE (
            Produto_Referencia VARCHAR(20),
            Quantidade INT,
            Armazem_Id INT
        );
        
        INSERT INTO @ItensAntigos (Produto_Referencia, Quantidade, Armazem_Id)
        SELECT 
            i.Produto_Referencia,
            i.Quantidade,
            l.Armazem_Id
        FROM Item i
        JOIN Venda v ON i.Venda_Id = v.Id
        JOIN Loja l ON v.Loja_Id = l.Id
        WHERE i.Venda_Id = @Venda_Id;
        
        UPDATE s
        SET s.Quantidade = s.Quantidade + ia.Quantidade
        FROM Stock s
        JOIN @ItensAntigos ia ON s.Produto_Referencia = ia.Produto_Referencia 
                              AND s.Armazem_Id = ia.Armazem_Id;
        
        DELETE FROM Item WHERE Venda_Id = @Venda_Id;
        
        UPDATE Venda
        SET 
            Cliente_Nif = @Cliente_Nif,
            MetodoPagamento = @MetodoPagamento
        WHERE Id = @Venda_Id;
        
        DECLARE @Loja_Id INT;
        DECLARE @Armazem_Id INT;
        
        SELECT @Loja_Id = Loja_Id FROM Venda WHERE Id = @Venda_Id;
        SELECT @Armazem_Id = Armazem_Id FROM Loja WHERE Id = @Loja_Id;
        
        INSERT INTO Item (Venda_Id, Produto_Referencia, Quantidade, PrecoUnit)
        SELECT 
            @Venda_Id,
            i.ProdutoRef,
            i.Quantidade,
            p.Preco
        FROM @Itens i
        JOIN Produto p ON i.ProdutoRef = p.Referencia;
        
        UPDATE s
        SET s.Quantidade = s.Quantidade - i.Quantidade
        FROM Stock s
        JOIN @Itens i ON s.Produto_Referencia = i.ProdutoRef
        WHERE s.Armazem_Id = @Armazem_Id;
        
        IF EXISTS (
            SELECT 1 
            FROM Stock s
            JOIN @Itens i ON s.Produto_Referencia = i.ProdutoRef
            WHERE s.Armazem_Id = @Armazem_Id AND s.Quantidade < 0
        )
        BEGIN
            THROW 50002, 'Stock insuficiente para um ou mais produtos.', 1;
        END
        
        
        COMMIT TRANSACTION;
        
        PRINT '✅ Venda editada com sucesso!';
        
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
            
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        THROW 50000, @ErrorMessage, 1;
    END CATCH
END
GO
