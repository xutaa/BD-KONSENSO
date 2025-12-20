-- =============================================
-- Tipo de Dados: ListaItensVenda
-- Descrição: Tipo de tabela para passar listas de itens de venda
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.types WHERE name = 'ListaItensVenda' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
    CREATE TYPE dbo.ListaItensVenda AS TABLE (
        ProdutoRef VARCHAR(20),
        Quantidade INT
    );
END
GO

-- =============================================
-- SP: RegistarVendaCompleta
-- Descrição: Regista uma venda e atualiza o stock correspondente
-- =============================================
CREATE OR ALTER PROCEDURE dbo.RegistarVendaCompleta
    @LojaId INT,
    @ClienteNif VARCHAR(15),
    @MetodoPagamento VARCHAR(50),
    @Itens dbo.ListaItensVenda READONLY
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @RealArmazemId INT;
    DECLARE @VendaId INT;
    DECLARE @ValorTotalVenda DECIMAL(18,2);

    SELECT @RealArmazemId = Armazem_Id FROM dbo.Loja WHERE Id = @LojaId;

    IF @RealArmazemId IS NULL
    BEGIN
        RAISERROR('Erro: Não foi encontrado um armazém válido para a Loja selecionada.', 16, 1);
        RETURN;
    END

    BEGIN TRANSACTION;
    BEGIN TRY
        IF EXISTS (
            SELECT 1 
            FROM (
                SELECT ProdutoRef, SUM(Quantidade) as QtdTotalPedida
                FROM @Itens 
                GROUP BY ProdutoRef
            ) AS CarrinhoAgregado
            LEFT JOIN dbo.Stock S ON CarrinhoAgregado.ProdutoRef = S.Produto_Referencia 
                AND S.Armazem_Id = @RealArmazemId
            WHERE ISNULL(S.Quantidade, 0) < CarrinhoAgregado.QtdTotalPedida
        )
        BEGIN
            THROW 50005, 'Venda Recusada: Um ou mais produtos não possuem stock suficiente nesta loja.', 1;
        END

        SELECT @ValorTotalVenda = SUM(L.Quantidade * P.Preco)
        FROM @Itens L
        JOIN dbo.Produto P ON L.ProdutoRef = P.Referencia;

        INSERT INTO dbo.Venda (DataHora, MetodoPagamento, Loja_Id, Cliente_Nif, ValorTotal)
        VALUES (GETDATE(), @MetodoPagamento, @LojaId, @ClienteNif, @ValorTotalVenda);
        
        SET @VendaId = SCOPE_IDENTITY();

        INSERT INTO dbo.Item (Venda_Id, Produto_Referencia, Quantidade, Preco)
        SELECT @VendaId, L.ProdutoRef, L.Quantidade, P.Preco
        FROM @Itens L
        JOIN dbo.Produto P ON L.ProdutoRef = P.Referencia;

        UPDATE S
        SET S.Quantidade = S.Quantidade - L.QtdAgregada
        FROM dbo.Stock S
        JOIN (
            SELECT ProdutoRef, SUM(Quantidade) as QtdAgregada 
            FROM @Itens GROUP BY ProdutoRef
        ) L ON S.Produto_Referencia = L.ProdutoRef
        WHERE S.Armazem_Id = @RealArmazemId;

        COMMIT TRANSACTION;
        SELECT @VendaId AS VendaId, 'SUCESSO' AS Status;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO
