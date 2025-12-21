-- =============================================
-- Trigger: AbaterStockVenda
-- Descrição: Abate automaticamente a quantidade no stock ao inserir itens numa venda.
-- Garante consistência entre vendas e stock sem intervenção da aplicação.
-- =============================================
CREATE OR ALTER TRIGGER AbaterStockVenda
ON dbo.Item
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Atualiza o stock cruzando informações de Item -> Venda -> Loja -> Armazém
    UPDATE S
    SET S.Quantidade = S.Quantidade - I.Quantidade
    FROM dbo.Stock S
    INNER JOIN inserted I ON S.Produto_Referencia = I.Produto_Referencia
    INNER JOIN dbo.Venda V ON I.Venda_Id = V.Id
    INNER JOIN dbo.Loja L ON V.Loja_Id = L.Id
    WHERE S.Armazem_Id = L.Armazem_Id;

    -- Nota: Se o stock ficar negativo, o trigger 'GarantirStockPositivo' 
    -- (se ativo) irá reverter esta transação automaticamente.
END
GO
