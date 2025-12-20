-- =============================================
-- Index: IX_Item_Produto
-- Descrição: Acelera pesquisas de itens por produto
-- =============================================
CREATE NONCLUSTERED INDEX IX_Item_Produto 
ON Item(Produto_Referencia) 
INCLUDE (Quantidade, Preco);
GO
